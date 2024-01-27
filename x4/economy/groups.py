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
                foundations("T1–T2: Food & Drugs").filter_by_tier({1, 2}),
                foundations("T3–T6: Construction").filter_by_tier({3, 4, 5, 6}),
                foundations("T3–T4: Refined and Advanced").filter_by_tier({3, 4}),
                foundations("T5–T6: Advanced and Components").filter_by_tier({4, 5}),
                foundations("T5–T6: Components and Equipment").filter_by_tier({5, 6}),
            ],
        ),
        EconomyGroup(
            title="Foundations: Argon, Paranid, and Teladi",
            economies=[
                food_and_drugs("T1–T2: Argon Food & Drugs", Hint.FULL_GRAPH_ONLY).with_single_recipe(["Argon"]),
                food_and_drugs("T1–T2: Paranid Food & Drugs", Hint.FULL_GRAPH_ONLY).with_single_recipe(["Paranid"]),
                food_and_drugs("T1–T2: Teladi Food & Drugs", Hint.FULL_GRAPH_ONLY).with_single_recipe(["Teladi"]),
                construction("T3–T6: Teladi Build Method").with_single_recipe(["Teladi", "Universal"]),
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
                construction("T3–T6: Terran Build Method").with_single_recipe(["Terran"]),
            ],
        ),
        EconomyGroup(
            title="Tides of Avarice",
            economies=[
                construction("T3–T6: Recycling Recipes").with_single_recipe(["Recycling"]),
                construction("T3–T6: Recycling Build Method").with_single_recipe(["Recycling", "Universal"]),
            ],
        ),
        EconomyGroup(
            title="Kingdom End",
            economies=[
                food_and_drugs("T1–T2: Boron Food & Drugs", Hint.FULL_GRAPH_ONLY).with_single_recipe(["Boron"]),
            ],
        ),
    ]
