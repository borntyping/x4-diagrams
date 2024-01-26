import dataclasses
import itertools
import pathlib
import re

import graphviz
import plotly.graph_objs
import structlog

from x4.economy.economy import Economy

logger = structlog.get_logger(logger_name=__name__)


@dataclasses.dataclass(frozen=True)
class Diagram:
    title: str
    subtitle: str
    image: pathlib.Path
    links: dict[str, pathlib.Path]


class Writer:
    @staticmethod
    def filename(economy: Economy, suffix: str, ext: str) -> str:
        name = re.sub(r"[^a-z0-9]", "_", economy.name.lower())
        name = re.sub("__+", "_", name)
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
        mapping = economy.as_dict()

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
            for input_ware in production.input_wares
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
        figure.update_layout(title_text=economy.name)
        return figure

    def render(self, economy: Economy) -> Diagram:
        logger.debug("Drawing economy with plotly", economy=economy)
        self.output_directory.mkdir(exist_ok=True)
        png = self.output_directory / self.filename(economy, "sankey", "png")
        html = self.output_directory / self.filename(economy, "sankey", "html")

        figure = self.plot(economy=economy)
        figure.write_html(html.as_posix(), include_plotlyjs="cdn")
        figure.write_image(png.as_posix(), width=1000, height=500)

        image = png.relative_to(self.output_directory)
        interactive = html.relative_to(self.output_directory)

        logger.warning("Drew economy with plotly", economy=repr(economy), image=image)
        return Diagram(
            title=economy.name,
            subtitle="Rendered with plotly",
            image=image,
            links={"Interactive": interactive, "Image": image},
        )


@dataclasses.dataclass(frozen=True)
class GraphvizWriter(Writer):
    output_directory: pathlib.Path

    def dot(self, economy: Economy) -> graphviz.Graph:
        fontname = "Helvetica,Arial,sans-serif"
        g = graphviz.Graph("X4 Economy")
        g.attr(fontname=fontname, compound="true")
        g.attr(
            "graph",
            pad="0.5",
            ranksep="2",
            nodesep="0.3",
        )
        g.attr(
            "node",
            fontname=fontname,
            penwidth="0",
            style="filled",
            color="slategray1",
            margin="0.2",
            shape="record",
        )
        g.attr(
            "edge",
            fontname=fontname,
            penwidth="2.5",
        )

        for tier, wares in itertools.groupby(economy.wares, key=lambda w: w.tier):
            with g.subgraph(name=str(tier.key)) as s:
                s.attr(label=tier.name, cluster="true")
                for resource in wares:
                    s.node(resource.name, colour=resource.graphviz_fillcolor(), shape="box")

        mapping = economy.as_dict()
        for output_ware in economy.wares:
            for recipe in output_ware.recipes:
                for i in recipe.input_wares:
                    if i.key not in mapping:
                        raise Exception(f"Input for {output_ware} not found in {economy}: {i.key}")

                    input_ware = mapping[i.key]
                    constraint = self.recipe_constraint(
                        recipe.method,
                        input_ware.name,
                        output_ware.name,
                    )
                    color = self.recipe_color(
                        recipe.method,
                        input_ware.name,
                        output_ware.name,
                    )
                    g.edge(
                        input_ware.name,
                        output_ware.name,
                        constraint=constraint,
                        color=color,
                    )
        return g

    @staticmethod
    def recipe_constraint(recipe: str, input_ware_name: str, output_ware_name: str) -> str:
        match (recipe, input_ware_name, output_ware_name):
            case (_, "Water", _):
                return "false"
            case (_, "Energy Cells", _):
                return "false"
            case (_, "Scrap Metal", _):
                return "false"
            case (_, _, "Medical Supplies"):
                return "false"
        return "true"

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

    def render(self, economy: Economy) -> Diagram:
        logger.debug("Drawing economy with graphviz", economy=economy)
        self.output_directory.mkdir(exist_ok=True)
        dot = self.dot(economy=economy)
        filename = self.filename(economy, "graph", "dot")
        outfile = self.output_directory / self.filename(economy, "graph", "png")
        path = dot.render(
            directory=self.output_directory,
            filename=filename,
            outfile=outfile,
            format="png",
        )

        image = pathlib.Path(path).relative_to(self.output_directory)
        source = (self.output_directory / filename).relative_to(self.output_directory)
        logger.info("Drew economy with graphviz", economy=repr(economy), image=image)
        return Diagram(
            title=economy.name,
            subtitle="Rendered with graphviz",
            image=image,
            links={"Image": image, "Source": source},
        )