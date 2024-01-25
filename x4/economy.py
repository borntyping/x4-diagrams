import dataclasses
import logging
import pathlib
import typing

import click
import graphviz
import plotly.graph_objs
import structlog

from x4.logs import configure_structlog_once
from x4.types import Economy, Method
from x4_data.economy import TIERS


logger = structlog.get_logger(logger_name=__name__)


@dataclasses.dataclass(frozen=True, repr=False)
class EconomyGraph(Economy):
    names: typing.Tuple[str, ...] = ()

    def __repr__(self):
        return "Economy<{}, {} tiers, {} wares>".format(
            self.title(),
            len(self.tiers),
            len(self.wares()),
        )

    def __str__(self) -> str:
        return self.title()

    def filename(self) -> str:
        return "-".join([x.lower() for x in self.names])

    def title(self) -> str:
        return " ".join(self.names)

    def consumption(self) -> typing.Self:
        return self.filter(names=["Consumption"], include_tier_keys={1, 2})

    def construction(self) -> typing.Self:
        return self.filter(names=["Construction"], include_tier_keys={3, 4, 5, 6})

    def harvested(self) -> typing.Self:
        return self.filter(names=["Harvested"], include_tier_keys={0})

    def basic_food(self) -> typing.Self:
        return self.filter(names=["Basic Food"], include_tier_keys={1})

    def food_and_drugs(self) -> typing.Self:
        return self.filter(names=["Food and Drugs"], include_tier_keys={2})

    def refined(self) -> typing.Self:
        return self.filter(names=["Refined"], include_tier_keys={3})

    def components(self) -> typing.Self:
        return self.filter(names=["Components"], include_tier_keys={5})

    def advanced(self) -> typing.Self:
        return self.filter(names=["Advanced"], include_tier_keys={4})

    def equipment(self) -> typing.Self:
        return self.filter(names=["Equipment"], include_tier_keys={6})

    def terminal(self) -> typing.Self:
        return self.filter(names=["Terminal"], include_tier_keys={7})

    def universal(self) -> typing.Self:
        return self.filter(names=["Universal"], methods=["Universal"])

    def terran(self) -> typing.Self:
        return self.filter(names=["Terran"], methods=["Terran"])

    def add_names(self, names: list[str]) -> typing.Self:
        return dataclasses.replace(self, names=(*self.names, *names))

    def filter(
        old,
        names: list[str],
        methods: list[Method] | None = None,
        exclusive: bool = False,
        include_tier_keys: set[int] | None = None,
    ) -> typing.Self:
        new = old.add_names(names)

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
            for production in target.production
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
                    "value": [link.value for link in links],
                    "label": [link.label for link in links],
                    # "color": [link.color for link in links],
                },
            )
        )
        figure.update_layout(title_text=economy.title())
        return figure

    def render(self, economy: typing.Iterable[EconomyGraph]) -> typing.Iterable[pathlib.Path]:
        self.output_directory.mkdir(exist_ok=True)
        for economy in economy:
            path = self.output_directory / f"{economy.filename()}.png"
            self.plot(economy=economy).write_image(path.as_posix())
            logger.warning(
                "Drew economy with plotly",
                economy=economy.title(),
                path=path.as_posix(),
            )
            yield pathlib.Path(path)


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
            for production in output_resource.production:
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

    def render(self, economies: typing.Iterable[EconomyGraph]) -> typing.Iterable[pathlib.Path]:
        self.output_directory.mkdir(exist_ok=True)
        for economy in economies:
            dot = self.dot(economy=economy)
            path = dot.render(
                directory=self.output_directory,
                filename=f"{economy.filename()}.dot",
                outfile=self.output_directory / f"{economy.filename()}.png",
                format="png",
            )
            logger.info("Drew economy with graphviz", economy=economy, path=path)
            yield pathlib.Path(path)


def breakdown() -> typing.Sequence[EconomyGraph]:
    economy = EconomyGraph(TIERS)
    economy = economy.remove_production_input("energy_cells")
    economy = economy.remove_production_input("water")

    universal_consumption = economy.universal().consumption()
    universal_construction = economy.universal().construction()

    terran_consumption = economy.terran().consumption()
    terran_construction = economy.terran().construction()

    teladi_consumption = economy.filter(names=["Teladi"], methods=["Teladi"]).consumption()
    teladi_construction = economy.filter(names=["Teladi"], methods=["Teladi", "Universal"]).construction()

    return [
        universal_consumption,
        universal_construction,
        terran_consumption,
        terran_construction,
        teladi_consumption,
        teladi_construction,
    ]


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
    writers = [
        PlotlyWriter(output_directory=output_directory / "sankey"),
        GraphvizWriter(output_directory=output_directory / "graphs"),
    ]

    economies = breakdown()

    paths = [path for writer in writers for path in writer.render(economies)]

    for path in paths:
        print(f'<img src="{path}" alt="{path.name}" style="width: 500px;">')


if __name__ == "__main__":
    configure_structlog_once()
    main()
