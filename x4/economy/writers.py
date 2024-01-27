import dataclasses
import html
import itertools
import pathlib
import re
import typing

import graphviz
import jinja2
import plotly.graph_objs
import structlog

from x4.economy.economy import Economy, Hint
from x4.economy.groups import EconomyGroup
from x4.types import Storage, Ware

logger = structlog.get_logger(logger_name=__name__)


@dataclasses.dataclass(frozen=True)
class Diagram:
    title: str
    description: typing.Tuple[str, ...]
    image: pathlib.Path
    links: dict[str, pathlib.Path]


@dataclasses.dataclass(frozen=True)
class EconomyOutput:
    title: str
    diagrams: typing.Sequence[Diagram]
    original: Economy


@dataclasses.dataclass(frozen=True)
class EconomyGroupOutput:
    title: str
    economies: typing.Sequence[EconomyOutput]
    original: EconomyGroup


class Writer:
    @staticmethod
    def filename(economy: Economy, suffixes: typing.Sequence[str], ext: str) -> str:
        name = re.sub(r"[^a-z0-9]", "_", economy.name.lower())
        name = re.sub("__+", "_", name)
        suffix = "_".join(suffixes)
        return "{}_{}.{}".format(name, suffix, ext)


@dataclasses.dataclass(frozen=True)
class PlotlyWriter(Writer):
    output_directory: pathlib.Path

    @dataclasses.dataclass(frozen=True)
    class Link:
        source: int
        target: int
        value: int
        label: str
        color: str

    def plot(self, economy: Economy):
        mapping = economy.wares_as_dict()

        if not mapping:
            raise Exception("Economy contains no resources")

        labels = [ware.name for ware in economy.wares]
        links = [
            self.Link(
                source=labels.index(mapping[input_ware.key].name),
                target=labels.index(target.name),
                value=input_ware.amount,
                label=production.method,
                color=production.plotly_colour(),
            )
            for target in economy.wares
            for production in target.recipes
            for input_ware in production.inputs
        ]

        figure = plotly.graph_objs.Figure(
            data=plotly.graph_objs.Sankey(
                arrangement="snap",
                node={
                    "label": [ware.name for ware in economy.wares],
                },
                link={
                    "source": [link.source for link in links],
                    "target": [link.target for link in links],
                    "value": [1 for link in links],
                    "label": [link.label for link in links],
                    # "color": [link.color for link in links],
                },
            )
        )

        figure.update_layout(
            title_text="{}<br><sup>{}</sup>".format(
                economy.name,
                " ".join(economy.description),
            ),
        )
        return figure

    def diagram(self, economy: Economy, filename_suffixes: typing.Sequence[str] = ()) -> Diagram:
        logger.debug("Drawing economy with plotly", economy=economy)
        self.output_directory.mkdir(exist_ok=True)
        png_path = self.output_directory / self.filename(economy, ("sankey", *filename_suffixes), "png")
        html_path = self.output_directory / self.filename(economy, ("sankey", *filename_suffixes), "html")

        figure = self.plot(economy=economy)
        figure.write_html(html_path.as_posix(), include_plotlyjs="cdn")
        figure.write_image(png_path.as_posix(), width=1000, height=500)

        image = png_path.relative_to(self.output_directory)
        interactive = html_path.relative_to(self.output_directory)

        logger.warning("Drew economy with plotly", economy=repr(economy))
        return Diagram(
            title=economy.name,
            description=(*economy.description, "Rendered with plotly."),
            image=image,
            links={"Interactive": interactive, "Image": image},
        )


@dataclasses.dataclass(frozen=True)
class GraphvizWriter(Writer):
    output_directory: pathlib.Path
    environment: jinja2.Environment

    def dot(self, economy: Economy) -> graphviz.Digraph:
        label_parts = [f"<b>{html.escape(economy.name)}</b>"]
        if economy.description:
            label_parts.append(f"<br/>")
        for line in economy.description:
            label_parts.append(f"<br/>{html.escape(line)}")

        fontname = "Helvetica,Arial,sans-serif"
        g = graphviz.Digraph("X4 Economy", edge_attr={"arrowType": "normal"})
        g.attr(fontname=fontname, compound="true")
        g.attr(label=f"<{''.join(label_parts)}>")
        g.attr(
            "graph",
            pad="0.5",
            ranksep="3",
            nodesep="0.3",
        )
        g.attr(
            "node",
            fontname=fontname,
            penwidth="2.0",
            # style="filled",
            color="slategray1",
            margin="0.2",
            shape="plaintext",
        )
        g.attr(
            "edge",
            fontname=fontname,
            penwidth="2.0",
            arrowhead="normal",
            arrowsize="1.0",
            headport="n",
            tailport="s",
        )

        mapping = economy.wares_as_dict()
        template = self.environment.get_template("ware.html")

        for tier, wares in itertools.groupby(economy.wares, key=lambda w: w.tier):
            with g.subgraph(name=str(tier.key)) as s:
                s.attr(label=str(tier), cluster="true")
                for ware in wares:
                    label = template.render(
                        ware=ware,
                        inputs=[mapping[key] for key in ware.inputs_as_set()],
                        outputs=economy.outputs_for_ware(ware),
                    )

                    s.node(ware.key, label=f"<{label}>")

        for output_ware in economy.wares:
            for recipe in output_ware.recipes:
                for i in recipe.inputs:
                    if i.key not in mapping:
                        raise Exception(f"Input for {output_ware} not found in {economy}: {i.key}")

                    input_ware = mapping[i.key]
                    color = self.recipe_color(
                        recipe.method,
                        input_ware.name,
                        output_ware.name,
                    )
                    g.edge(
                        f"{input_ware.key}:{output_ware.key}:s",
                        f"{output_ware.key}:{input_ware.key}:n",
                        color=input_ware.colour,
                        weight=self.weight(input_ware=input_ware, output_ware=output_ware),
                        arrowhead=self.arrowhead(input_ware.storage),
                    )
        return g

    @staticmethod
    def arrowhead(storage: Storage | None) -> str:
        if storage == "Container":
            return "box"
        elif storage == "Liquid":
            return "odot"
        elif storage == "Solid":
            return "empty"
        elif storage == "Condensate":
            return "invempty"
        elif storage is None:
            return "none"

        raise ValueError(storage)

    def weight(self, input_ware: Ware, output_ware: Ware) -> str:
        match (input_ware, output_ware):
            case (Ware(key="energy_cells"), _):
                return "0.1"
            case (Ware(key="water"), _):
                return "0.1"

        return "1.0"

    @staticmethod
    def recipe_color(recipe: str, input_ware_name: str, output_ware_name: str) -> str:
        match (recipe, input_ware_name, output_ware_name):
            case (_, "Water" | "Energy Cells", _):
                return "azure2"
            case (_, _, "Medical Supplies"):
                return "azure2"
            case (_, "Scrap Metal", _):
                return "red"
            case (_, "Refined Metals", _):
                return "firebrick"
            case (_, "Teladianium", _) | ("Teladi", _, _):
                return "goldenrod"
        return "slategray4"

    def diagram(self, economy: Economy, filename_suffixes: typing.Sequence[str] = ()) -> Diagram:
        logger.debug("Drawing economy with graphviz", economy=economy)
        self.output_directory.mkdir(exist_ok=True)
        dot = self.dot(economy=economy)
        filename = self.filename(economy, ("graph", *filename_suffixes), "dot")
        outfile = self.output_directory / self.filename(economy, ("graph", *filename_suffixes), "png")
        path = dot.render(
            directory=self.output_directory,
            filename=filename,
            outfile=outfile,
            format="png",
        )

        image = pathlib.Path(path).relative_to(self.output_directory)
        source = (self.output_directory / filename).relative_to(self.output_directory)
        logger.info("Drew economy with graphviz", economy=repr(economy))
        return Diagram(
            title=economy.name,
            description=(*economy.description, "Rendered with graphviz."),
            image=image,
            links={"Image": image, "Source": source},
        )


@dataclasses.dataclass(frozen=True)
class IndexWriter:
    output_directory: pathlib.Path
    environment: jinja2.Environment

    def index(self, groups: typing.Sequence[EconomyGroupOutput]) -> pathlib.Path:
        template = self.environment.get_template("index.html")
        rendered = template.render(groups=groups)
        path = self.output_directory / "index.html"
        path.write_text(rendered)
        logger.warning("Rendered index", path=path)
        return path


@dataclasses.dataclass(frozen=True)
class Builder:
    graphviz_writer: GraphvizWriter
    plotly_writer: PlotlyWriter
    index_writer: IndexWriter

    def economy_group(self, group: EconomyGroup) -> EconomyGroupOutput:
        return EconomyGroupOutput(
            title=group.title,
            economies=[self.economy(economy) for economy in group.economies],
            original=group,
        )

    def economy(self, economy: Economy) -> EconomyOutput:
        return EconomyOutput(
            title=economy.name,
            diagrams=tuple(self.diagrams(economy)),
            original=economy,
        )

    def diagrams(self, economy: Economy) -> typing.Iterable[Diagram]:
        if economy.hints in Hint.SIMPLIFY_INCLUSIVE | Hint.SIMPLIFY_EXCLUSIVE:
            simplified = economy.remove_common_inputs()
            yield self.graphviz_writer.diagram(simplified, filename_suffixes=("simplified",))
            yield self.plotly_writer.diagram(simplified, filename_suffixes=("simplified",))

        if economy.hints not in Hint.SIMPLIFY_EXCLUSIVE:
            yield self.graphviz_writer.diagram(economy)
            yield self.plotly_writer.diagram(economy)

    def main(self, groups: typing.Sequence[EconomyGroup]) -> pathlib.Path:
        return self.index_writer.index([self.economy_group(group) for group in groups])
