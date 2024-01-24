import dataclasses
import logging
import pathlib
import typing

import click
import graphviz
import plotly.graph_objs
import structlog

from x4.types import Method, Ware, Tier
from x4_data.economy import TIERS


logger = structlog.get_logger()


@dataclasses.dataclass(frozen=True)
class EconomyGraph:
    tiers: typing.Sequence[Tier]
    selected_variant: str = "Universal"

    def resources(self) -> typing.Mapping[str, Ware]:
        return {resource.identifier: resource for tier in self.tiers for resource in tier.wares}

    def select_recipe(self, variant: str) -> typing.Self:
        return dataclasses.replace(self, selected_variant=variant)

    def include_tiers(self, levels: set[int]) -> typing.Self:
        logger.debug("Filtering economy graph by tier", include_tiers=levels)
        resources = self.resources()
        tiers = [t for t in self.tiers if t.level in levels]

        # Select resources in the given tiers.
        selected = {r.identifier for t in tiers for r in t.wares}

        # Select the dependencies of those resources.
        dependencies = {i for i in selected for i in resources[i].dependencies()}

        include = selected | dependencies
        tiers = [t.filter_resources(include=include, exclude=set()) for t in self.tiers]
        return dataclasses.replace(self, tiers=tiers)

    def include_methods(self, method: Method) -> typing.Self:
        logger.debug("Filtering economy graph by build method", method=method)
        tiers = [t.filter_methods(method=method) for t in self.tiers]
        return dataclasses.replace(self, tiers=tiers)

    def exclude_resources(self, exclude: set[str] = frozenset()) -> typing.Self:
        logger.debug("Filtering economy graph by resource")
        include = {r for r in self.resources()}
        tiers = [t.filter_resources(include=include, exclude=exclude) for t in self.tiers]
        return dataclasses.replace(self, tiers=tiers)


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

    def plot(self, economy: EconomyGraph, title_text: str):
        resources = {resource.identifier: resource for tier in economy.tiers for resource in tier.wares}
        if not resources:
            exit()

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
            for production in target.production
            for source, value in production.wares.items()
        ]

        figure = plotly.graph_objs.Figure(
            data=plotly.graph_objs.Sankey(
                arrangement="snap",
                node={
                    "label": [resource.name for resource in economy.resources().values()],
                },
                link={
                    "source": [link.source for link in links],
                    "target": [link.target for link in links],
                    "value": [link.value for link in links],
                    "label": [link.label for link in links],
                    # "color": [link.color for link in links],
                },
            )
        )
        figure.update_layout(title_text=title_text)
        return figure

    def __call__(self, filename: str, economy: EconomyGraph, title_text: str) -> None:
        self.output_directory.mkdir(exist_ok=True)
        path = self.output_directory / filename
        self.plot(economy=economy, title_text=title_text).write_image(path.as_posix())
        logger.info("Drew economy graph with plotly", title_text=title_text, filename=filename)


@dataclasses.dataclass(frozen=True)
class GraphvizWriter:
    output_directory: pathlib.Path

    def dot(self, economy: EconomyGraph) -> str:
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
                    s.node(resource.name, colour=resource.fillcolor())

        resources = economy.resources()
        for output_resource in resources.values():
            for production in output_resource.production:
                for input_resource_id, amount in production.wares.items():
                    input_resource = resources[input_resource_id]
                    constraint = self.recipe_constraint(production.method, input_resource.name, output_resource.name)
                    color = self.recipe_color(production.method, input_resource.name, output_resource.name)
                    g.edge(
                        input_resource.name,
                        output_resource.name,
                        constraint=constraint,
                        color=color,
                    )
        return g.source

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

    def __call__(self, filename: str, economy: EconomyGraph) -> None:
        self.output_directory.mkdir(exist_ok=True)
        path = self.output_directory / filename
        path.write_text(self.dot(economy=economy))
        logger.info("Drew economy graph with graphviz", filename=filename)


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
    economy = EconomyGraph(tiers=TIERS)
    economy = economy.exclude_resources({"energy_cells"})

    food_and_drugs = economy.include_tiers({1, 2})
    refined = economy.include_tiers({3})
    advanced = economy.include_tiers({3, 4})
    components = economy.include_tiers({5})
    equipment = economy.include_tiers({6})
    construction = economy.include_tiers({3, 4, 5, 6})

    p = PlotlyWriter(output_directory=output_directory / "plotly")
    p("economy-food-and-drugs.png", food_and_drugs, title_text="Food & Drugs")
    p("economy-3-refined.png", refined, title_text="Refined")
    p("economy-4-advanced.png", advanced, title_text="Advanced")
    p("economy-5-components.png", components, title_text="Components")
    p("economy-6-equipment.png", equipment, title_text="Equipment")
    p("economy-construction.png", construction, title_text="Construction")

    g = GraphvizWriter(output_directory=output_directory / "graphviz")
    g("economy-food-and-drugs.dot", food_and_drugs)
    g("economy-3-refined.dot", refined)
    g("economy-4-advanced.dot", advanced)
    g("economy-5-components.dot", components)
    g("economy-6-equipment.dot", equipment)


if __name__ == "__main__":
    structlog.stdlib.recreate_defaults(log_level=logging.INFO)
    main()
