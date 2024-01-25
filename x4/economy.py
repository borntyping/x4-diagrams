import dataclasses
import logging
import pathlib
import typing

import click
import graphviz
import jinja2
import plotly.graph_objs
import structlog

from x4.logs import configure_structlog_once
from x4.types import Economy, Method
from x4_data.economy import COMMONWEALTH_METHODS, TIERS


logger = structlog.get_logger(logger_name=__name__)


@dataclasses.dataclass(frozen=True, repr=False)
class EconomyGraph(Economy):
    name: str = "X4"
    group: str = "X4"

    def __repr__(self):
        return "Economy<{}, {} tiers, {} wares>".format(
            self.title(),
            len(self.tiers),
            len(self.wares()),
        )

    def __str__(self) -> str:
        return self.title()

    def filename(self, suffix: str, ext: str) -> str:
        name = self.name.lower().replace(" ", "_")
        return "{}_{}.{}".format(name, suffix, ext)

    def title(self) -> str:
        return self.name

    def consumption(self) -> typing.Self:
        return self.filter(name="Consumption", include_tier_keys={1, 2})

    def construction(self) -> typing.Self:
        return self.filter(name="Construction", include_tier_keys={0, 3, 4, 5, 6})

    def harvested(self) -> typing.Self:
        return self.filter(name="Harvested", include_tier_keys={0})

    def basic_food(self) -> typing.Self:
        return self.filter(name="Basic Food", include_tier_keys={1})

    def food_and_drugs(self) -> typing.Self:
        return self.filter(name="Food and Drugs", include_tier_keys={2})

    def refined(self) -> typing.Self:
        return self.filter(name="Refined", include_tier_keys={3})

    def components(self) -> typing.Self:
        return self.filter(name="Components", include_tier_keys={5})

    def advanced(self) -> typing.Self:
        return self.filter(name="Advanced", include_tier_keys={4})

    def equipment(self) -> typing.Self:
        return self.filter(name="Equipment", include_tier_keys={6})

    def terminal(self) -> typing.Self:
        return self.filter(name="Terminal", include_tier_keys={7})

    def with_name(self, name: str) -> typing.Self:
        return dataclasses.replace(self, name=name)

    def with_group(self, group: str) -> typing.Self:
        return dataclasses.replace(self, group=group)

    def filter(
        self,
        group: str | None = None,
        name: str = None,
        *,
        methods: typing.Sequence[Method] | None = None,
        exclusive: bool = False,
        include_tier_keys: set[int] | None = None,
    ) -> typing.Self:
        new = self

        if name is not None:
            new = new.with_name(name)

        if group is not None:
            new = new.with_group(group)

        logger.debug(
            "Filtering economy",
            title=new.title(),
            methods=methods,
            exclusive=exclusive,
            filter_tiers=include_tier_keys,
        )

        if include_tier_keys is not None:
            new = new.include_tiers(include_tier_keys)

        if methods is not None:
            new = new.filter_production_methods_and_unused_wares(methods)

        new.validate()

        logger.info(
            "Filtered economy",
            title=new.title(),
            methods=methods,
            exclusive=exclusive,
            filter_tiers=include_tier_keys,
        )

        return new


def breakdown() -> typing.Sequence[EconomyGraph]:
    economy = EconomyGraph(TIERS)
    economy = economy.remove_production_input("energy_cells")
    economy = economy.remove_production_input("water")

    consumption = economy.consumption()
    construction = economy.construction()

    commonwealth_consumption = consumption.filter("Commonwealth", "Commonwealth construction", methods=COMMONWEALTH_METHODS)
    universal_construction = construction.filter("Commonwealth", "Universal construction", methods=["Universal"])

    terran_consumption = consumption.filter("Cradle of Humanity", "Terran", methods=["Terran"])
    terran_construction = construction.filter("Cradle of Humanity", "Terran", methods=["Terran"])

    teladi_consumption = consumption.filter("Teladi", "Teladi consumption", methods=["Teladi"])
    teladi_construction = construction.filter("Teladi", "Teladi construction", methods=["Teladi", "Universal"])

    recycling = economy.filter("Tides of Avarice", "Scrap", methods=["Recycling"])
    recycling_construction = construction.filter("Tides of Avarice", "Scrap construction", methods=["Recycling", "Universal"])

    return [
        commonwealth_consumption,
        universal_construction,
        teladi_consumption,
        teladi_construction,
        terran_consumption,
        terran_construction,
        recycling,
        recycling_construction,
    ]


@dataclasses.dataclass(frozen=True)
class Diagram:
    group: str
    title: str
    subtitle: str
    image: pathlib.Path
    links: dict[str, pathlib.Path]


@dataclasses.dataclass(frozen=True)
class PlotlyWriter:
    output_directory: pathlib.Path

    @dataclasses.dataclass(frozen=True)
    class Link:
        source: int
        target: int
        value: int
        label: str
        color: str

    def plot(self, economy: EconomyGraph):
        resources = {resource.key: resource for tier in economy.tiers for resource in tier.wares}

        if not resources:
            raise Exception("Economy contains no resources")

        labels = [resource.name for resource in resources.values()]
        links = [
            self.Link(
                source=labels.index(resources[source].name),
                target=labels.index(target.name),
                value=value,
                label=production.method,
                color=production.colour(),
            )
            for tier in economy.tiers
            for target in tier.wares
            for production in target.recipes
            for source, value in production.wares.items()
        ]

        figure = plotly.graph_objs.Figure(
            data=plotly.graph_objs.Sankey(
                arrangement="snap",
                node={
                    "label": [resource.name for resource in economy.wares().values()],
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
        figure.update_layout(title_text=economy.title())
        return figure

    def render(self, economy: EconomyGraph) -> Diagram:
        self.output_directory.mkdir(exist_ok=True)
        png = self.output_directory / economy.filename("sankey", "png")
        html = self.output_directory / economy.filename("sankey", "html")

        figure = self.plot(economy=economy)
        figure.write_html(html.as_posix())
        figure.write_image(png.as_posix(), width=1000, height=500)
        logger.warning(
            "Drew economy with plotly",
            economy=economy.title(),
            png=png.as_posix(),
            html=html.as_posix(),
        )

        image = png.relative_to(self.output_directory)
        interactive = html.relative_to(self.output_directory)
        return Diagram(
            group=economy.group,
            title=economy.title(),
            subtitle="Rendered with plotly",
            image=image,
            links={"Interactive": interactive, "Image": image},
        )


@dataclasses.dataclass(frozen=True)
class GraphvizWriter:
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

        for tier in economy.tiers:
            with g.subgraph(name=str(tier.level)) as s:
                s.attr(label=str(tier), cluster="true")
                for resource in tier.wares:
                    s.node(resource.name, colour=resource.fillcolor(), shape="box")

        resources = economy.wares()
        for output_resource in resources.values():
            for production in output_resource.recipes:
                for input_resource_id, amount in production.wares.items():
                    input_resource = resources[input_resource_id]
                    constraint = self.recipe_constraint(
                        production.method,
                        input_resource.name,
                        output_resource.name,
                    )
                    color = self.recipe_color(
                        production.method,
                        input_resource.name,
                        output_resource.name,
                    )
                    g.edge(
                        input_resource.name,
                        output_resource.name,
                        constraint=constraint,
                        color=color,
                    )
        return g

    @staticmethod
    def recipe_constraint(recipe: str, input_resource_name: str, output_resource_name: str) -> str:
        match (recipe, input_resource_name, output_resource_name):
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
    def recipe_color(recipe: str, input_resource_name: str, output_resource_name: str) -> str:
        match (recipe, input_resource_name, output_resource_name):
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

    def render(self, economy: EconomyGraph) -> Diagram:
        self.output_directory.mkdir(exist_ok=True)
        dot = self.dot(economy=economy)
        filename = economy.filename("graph", "dot")
        outfile = self.output_directory / economy.filename("graph", "png")
        path = dot.render(
            directory=self.output_directory,
            filename=filename,
            outfile=outfile,
            format="png",
        )
        logger.info("Drew economy with graphviz", economy=economy, path=path)

        image = pathlib.Path(path).relative_to(self.output_directory)
        source = (self.output_directory / filename).relative_to(self.output_directory)
        return Diagram(
            group=economy.group,
            title=economy.title(),
            subtitle="Rendered with graphviz",
            image=image,
            links={"Image": image, "Source": source},
        )


def render_diagrams(output_directory: pathlib.Path, economies: typing.Sequence[EconomyGraph]) -> typing.Iterable[Diagram]:
    graphviz_writer = GraphvizWriter(output_directory=output_directory)
    plotly_writer = PlotlyWriter(output_directory=output_directory)

    for economy in economies:
        yield graphviz_writer.render(economy)
        yield plotly_writer.render(economy)


def render_index(output_directory: pathlib.Path, diagrams: list[Diagram]) -> pathlib.Path:
    for d in diagrams:
        assert d.group, d

    loader = jinja2.FileSystemLoader(pathlib.Path(__file__).with_name("templates"))
    environment = jinja2.Environment(loader=loader, undefined=jinja2.StrictUndefined)
    template = environment.get_template("index.html")
    rendered = template.render(diagrams=diagrams)
    path = output_directory / "index.html"
    path.write_text(rendered)
    logger.warning("Rendered index", path=path, diagrams=len(diagrams))
    return path


@click.command(name="economy")
@click.option(
    "--output-directory",
    default="docs",
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
        path_type=pathlib.Path,
    ),
)
def main(output_directory: pathlib.Path):
    economies = breakdown()
    diagrams = list(render_diagrams(output_directory, economies=economies))
    render_index(output_directory, diagrams=diagrams)


if __name__ == "__main__":
    configure_structlog_once()
    main()
