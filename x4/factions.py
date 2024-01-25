import dataclasses
import itertools
import typing

import graphviz

from x4 import docs
from x4.types import Faction
from x4_data.factions import ALIENS, FACTIONS, PIRATES


def factions_grouped_by_race() -> typing.Sequence[typing.Tuple[str, list[Faction]]]:
    sorted_factions = sorted(FACTIONS, key=lambda f: f.race.name)
    grouped_factions = itertools.groupby(sorted_factions, key=lambda f: f.race.name)
    return [(name, list(factions)) for name, factions in grouped_factions]


def connections(
    factions: typing.Iterable[Faction],
    get_others: typing.Callable[[Faction], typing.Iterable[str]],
) -> typing.Set[typing.Tuple[str, str]]:
    return {tuple(sorted((faction.tag, other))) for faction in factions for other in get_others(faction)}


def filter_factions(
    factions: typing.Sequence[Faction], excluded_factions: typing.Collection[Faction]
) -> typing.Sequence[Faction]:
    excluded_tags = [f.tag for f in excluded_factions]
    return [
        dataclasses.replace(
            faction,
            allies=[x for x in faction.allies if x not in excluded_tags],
            enemies=[x for x in faction.enemies if x not in excluded_tags],
            hostiles=[x for x in faction.hostiles if x not in excluded_tags],
        )
        for faction in factions
        if faction.tag not in excluded_tags
    ]


def graph(
    group_by_race: bool = True,
    show_allies: bool = True,
    show_enemies: bool = False,
    show_hostiles: bool = True,
    exclude_aliens: bool = True,
    exclude_pirates: bool = True,
) -> str:
    excluded_factions: list[Faction] = []
    if exclude_aliens:
        excluded_factions.extend(ALIENS)
    if exclude_pirates:
        excluded_factions.extend(PIRATES)
    factions = filter_factions(FACTIONS, excluded_factions)

    dot = graphviz.Digraph(comment="X4 Factions")
    dot.attr(fontname="Helvetica,Arial,sans-serif")
    dot.attr("graph", pad="0.5", ranksep="2", nodesep="0.3")
    dot.attr("node", fontname="Helvetica,Arial,sans-serif", penwidth="0", style="filled", linecolor="black", margin="0.2")
    dot.attr("edge", fontname="Helvetica,Arial,sans-serif", penwidth="2.5")

    if group_by_race:
        for index, (race_name, race_factions) in enumerate(factions_grouped_by_race()):
            with dot.subgraph(name=race_name) as sub:
                sub.attr(label=race_name)
                sub.attr(cluster="true")
                for faction in race_factions:
                    sub.node(faction.tag, label=str(faction), shape="box", fillcolor="lightsteelblue2")
    else:
        for faction in factions:
            dot.node(faction.tag, label=str(faction), shape="box", fillcolor="lightsteelblue2")

    if show_allies:
        for a, b in connections(factions, lambda f: f.allies):
            dot.edge(a, b, dir="both", color="green")

    if show_enemies:
        for a, b in connections(factions, lambda f: f.enemies):
            dot.edge(a, b, dir="both", color="pink")

    if show_hostiles:
        for a, b in connections(factions, lambda f: f.hostiles):
            dot.edge(a, b, dir="both", color="red")

    return dot.unflatten(stagger=2).source


def main() -> None:
    (docs / "factions.dot").write_text(graph())


if __name__ == "__main__":
    main()
