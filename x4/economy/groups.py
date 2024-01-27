import dataclasses
import typing

from x4.economy.economy import Economy, Hint
from x4.types import Method
from x4_data.economy import TIER_3, TIER_4, TIER_5, TIER_6, WARES


@dataclasses.dataclass(frozen=True)
class EconomyGroup:
    title: str
    economies: typing.Sequence[Economy]


def groups() -> typing.Sequence[EconomyGroup]:
    world = Economy()

    food_and_drugs = world.with_name("T1–T2: Food & Drugs").filter_by_tier({1, 2})
    construction = world.with_name("T3–T6: Construction").filter_by_tier({3, 4, 5, 6})

    commonwealth: set[Method] = {"Universal", "Argon", "Boron", "Paranid", "Split", "Teladi"}
    foundations = world.with_name("Foundations").with_selected_recipes(commonwealth)

    return [
        EconomyGroup(
            title="Foundations",
            economies=[
                foundations("T3–T6: Construction").filter_by_tier({3, 4, 5, 6}),
                foundations(str(TIER_3)).filter_by_tier({3}),
                foundations(str(TIER_4)).filter_by_tier({4}),
                foundations(str(TIER_5)).filter_by_tier({5}),
                foundations(str(TIER_6)).filter_by_tier({6}),
                foundations("T1–T2: Food & Drugs").filter_by_tier({1, 2}),
                food_and_drugs("T1–T2: Argon Food & Drugs", Hint.FULL_GRAPH_ONLY).with_single_recipe(["Argon"]),
                food_and_drugs("T1–T2: Paranid Food & Drugs", Hint.FULL_GRAPH_ONLY).with_single_recipe(["Paranid"]),
                food_and_drugs("T1–T2: Teladi Food & Drugs", Hint.FULL_GRAPH_ONLY).with_single_recipe(["Teladi"]),
                construction("T3–T6: Teladi Construction").with_single_recipe(["Teladi", "Universal"]),
            ],
        ),
        EconomyGroup(
            title="Split Vendetta",
            economies=[
                food_and_drugs("T1–T2: Split Food & Drugs", Hint.FULL_GRAPH_ONLY).with_single_recipe(["Split"]),
            ],
        ),
        EconomyGroup(
            title="Cradle of Humanity",
            economies=[
                food_and_drugs("T1–T2: Terran Food & Drugs", Hint.FULL_GRAPH_ONLY).with_single_recipe(["Terran"]),
                construction("T3–T6: Terran Construction").with_single_recipe(["Terran"]),
            ],
        ),
        EconomyGroup(
            title="Tides of Avarice",
            economies=[
                construction("T3–T6: Scrapping Construction").with_single_recipe(["Recycling"]),
                construction("T3–T6: Scrapping Construction").with_single_recipe(["Recycling", "Universal"]),
            ],
        ),
        EconomyGroup(
            title="Kingdom End",
            economies=[
                food_and_drugs("T1–T2: Boron Food & Drugs", Hint.FULL_GRAPH_ONLY).with_single_recipe(["Boron"]),
            ],
        ),
    ]
