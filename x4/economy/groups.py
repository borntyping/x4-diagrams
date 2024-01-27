import dataclasses
import typing

from x4.colours import Palette
from x4.economy.economy import BuildMethodEdgeColour, Economy, Hint
from x4.types import Method
from x4_data.economy import TIER_3, TIER_4, TIER_5, TIER_6, WARES
from x4_data.races import TELADI


@dataclasses.dataclass(frozen=True)
class EconomyGroup:
    title: str
    economies: typing.Sequence[Economy]


def groups() -> typing.Sequence[EconomyGroup]:
    world = Economy()

    food_and_drugs = world.with_name("T1–T2: Food & Drugs").select_tiers({1, 2}).verify()
    construction = world.with_name("T3–T6: Construction").select_tiers({3, 4, 5, 6}).verify()

    commonwealth: set[Method] = {"Universal", "Argon", "Boron", "Paranid", "Split", "Teladi"}
    foundations = world.with_name("Foundations").select_recipes(methods=commonwealth)

    return [
        EconomyGroup(
            title="Foundations",
            economies=[
                foundations("T1–T2: Food & Drugs").select_tiers({1, 2}),
                foundations("T3–T6: Construction").select_tiers({3, 4, 5, 6}),
                foundations("T3–T4: Refined and Advanced").select_tiers({3, 4}),
                foundations("T5–T6: Advanced and Components").select_tiers({4, 5}),
                foundations("T5–T6: Components and Equipment").select_tiers({5, 6}),
            ],
        ),
        EconomyGroup(
            title="Foundations: Argon, Paranid, and Teladi",
            economies=[
                food_and_drugs("T1–T2: Argon Food & Drugs", Hint.FULL_GRAPH_ONLY).select_recipe(["Argon"]),
                food_and_drugs("T1–T2: Paranid Food & Drugs", Hint.FULL_GRAPH_ONLY).select_recipe(["Paranid"]),
                food_and_drugs("T1–T2: Teladi Food & Drugs", Hint.FULL_GRAPH_ONLY).select_recipe(["Teladi"]),
                (
                    construction("T3–T6: Teladi Build Method")
                    .select_recipe(["Teladi", "Universal"])
                    .highlight_build_method("Teladi")
                ),
            ],
        ),
        EconomyGroup(
            title="Split Vendetta",
            economies=[
                food_and_drugs("T1–T2: Split Food & Drugs", Hint.FULL_GRAPH_ONLY).select_recipe(["Split"]),
            ],
        ),
        EconomyGroup(
            title="Cradle of Humanity",
            economies=[
                food_and_drugs("T1–T2: Terran Food & Drugs", Hint.FULL_GRAPH_ONLY).select_recipe(["Terran"]),
                construction("T3–T6: Terran Build Method").select_recipe(["Terran"]),
            ],
        ),
        EconomyGroup(
            title="Tides of Avarice",
            economies=[
                construction("T3–T6: Recycling Recipes").select_recipes(methods={"Recycling+Universal", "Recycling+Terran"}),
                (
                    construction("T3–T6: Recycling Build Method (Universal)")
                    .select_recipe(["Recycling+Universal", "Universal"])
                    .highlight_build_method("Recycling+Universal")
                ),
                (
                    construction("T3–T6: Recycling Build Method (Terran)")
                    .select_recipe(["Recycling+Terran", "Terran"])
                    .highlight_build_method("Recycling+Terran")
                ),
            ],
        ),
        EconomyGroup(
            title="Kingdom End",
            economies=[
                food_and_drugs("T1–T2: Boron Food & Drugs", Hint.FULL_GRAPH_ONLY).select_recipe(["Boron"]),
            ],
        ),
    ]
