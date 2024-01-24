import dataclasses
import pathlib
import typing

import click
import graphviz

from x4.types import Resource, Tier
from x4_data.economy import TIERS


@dataclasses.dataclass(frozen=True)
class EconomyGraph:
    tiers: typing.Sequence[Tier]
    selected_variant: str = "Universal"

    def resources(self) -> typing.Mapping[str, Resource]:
        return {resource.id: resource for tier in self.tiers for resource in tier.resources}

    def select_recipe(self, variant: str) -> typing.Self:
        return dataclasses.replace(self, selected_variant=variant)

    def select_tiers(self, *levels: int) -> typing.Self:
        mapping = {resource.name: resource for tier in self.tiers for resource in tier.resources}

        for tier in self.tiers:
            for resource in tier.resources:
                assert isinstance(resource, Resource)

        selected = [resource.name for tier in self.tiers for resource in tier.resources if tier.level in levels]
        dependencies = [i for r in selected for i in mapping[r].all_inputs()]
        resources = set(selected) | set(dependencies)

        tiers = [tier.filter_resources(resources) for tier in self.tiers]
        return dataclasses.replace(self, tiers=tiers)


@dataclasses.dataclass(frozen=True)
class EconomyGraphWriter:
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
                for resource in tier.resources:
                    s.node(resource.name, colour=resource.fillcolor())

        for output_resource in economy.resources().values():
            for recipe, input_resource_name in output_resource.inputs():
                constraint = self.recipe_constraint(recipe, input_resource_name, output_resource.name)
                color = self.recipe_color(recipe, input_resource_name, output_resource.name)
                g.edge(
                    input_resource_name,
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


@click.command(name="economy")
@click.option(
    "--output-directory",
    default="output",
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
        path_type=pathlib.Path,
    ),
)
def main(output_directory: pathlib.Path):
    writer = EconomyGraphWriter(output_directory=output_directory)
    economy = EconomyGraph(tiers=TIERS)

    writer("economy-2-food-and-drugs.dot", economy.select_tiers(1, 2))
    writer("economy-3-refined.dot", economy.select_tiers(3))
    writer("economy-4-advanced.dot", economy.select_tiers(3, 4))
    writer("economy-5-components.dot", economy.select_tiers(5))
    writer("economy-6-equipment.dot", economy.select_tiers(6))


if __name__ == "__main__":
    main()
