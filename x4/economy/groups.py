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
    world = Economy().done()

    food_and_drugs = world.with_name("T1–T2: Food & Drugs").filter_by_tier({1, 2}).done()
    construction = world.with_name("T3–T6: Construction").filter_by_tier({3, 4, 5, 6}).done()

    universal = world.with_name("Universal").with_single_recipe(["Universal"]).done()
    commonwealth: list[Method] = ["Universal", "Argon", "Boron", "Paranid", "Split", "Teladi"]

    return [
        EconomyGroup(
            title="Foundations",
            economies=[
                universal.with_name("T3–T6: Construction").filter_by_tier({3, 4, 5, 6}).with_hints(Hint.SIMPLIFY_EXCLUSIVE),
                universal.with_name(str(TIER_3)).filter_by_tier({3}).done(),
                universal.with_name(str(TIER_4)).filter_by_tier({4}).with_hints(Hint.SIMPLIFY_EXCLUSIVE).done(),
                universal.with_name(str(TIER_5)).filter_by_tier({5}).with_hints(Hint.SIMPLIFY_EXCLUSIVE).done(),
                universal.with_name(str(TIER_6)).filter_by_tier({6}).with_hints(Hint.SIMPLIFY_EXCLUSIVE).done(),
                (
                    food_and_drugs.with_name("T1–T2: Food & Drugs")
                    .with_selected_recipes(set(commonwealth))
                    .with_hints(Hint.SIMPLIFY_INCLUSIVE)
                    .done()
                ),
                food_and_drugs.with_name("T1–T2: Argon Food & Drugs").with_single_recipe(["Argon"]).done(),
                food_and_drugs.with_name("T1–T2: Paranid Food & Drugs").with_single_recipe(["Paranid"]).done(),
                food_and_drugs.with_name("T1–T2: Teladi Food & Drugs").with_single_recipe(["Teladi"]).done(),
                (
                    construction.with_name("T3–T6: Teladi Construction")
                    .with_single_recipe(["Teladi", "Universal"])
                    .with_hints(Hint.SIMPLIFY_EXCLUSIVE)
                    .done()
                ),
            ],
        ),
        EconomyGroup(
            title="Split Vendetta",
            economies=[
                food_and_drugs.with_name("T1–T2: Split Food & Drugs").with_single_recipe(["Split"]).done(),
            ],
        ),
        EconomyGroup(
            title="Cradle of Humanity",
            economies=[
                food_and_drugs.with_name("T1–T2: Terran Food & Drugs").with_single_recipe(["Terran"]).done(),
                construction.with_name("T3–T6: Terran Construction").with_single_recipe(["Terran"]).done(),
            ],
        ),
        EconomyGroup(
            title="Tides of Avarice",
            economies=[
                (
                    construction.with_name("T3–T6: Scrapping Construction")
                    .with_single_recipe(["Recycling"])
                    .with_hints(Hint.SIMPLIFY_EXCLUSIVE)
                    .done()
                ),
                (
                    construction.with_name("T3–T6: Scrapping Construction")
                    .with_single_recipe(["Recycling", "Universal"])
                    .with_hints(Hint.SIMPLIFY_EXCLUSIVE)
                    .done()
                ),
            ],
        ),
        EconomyGroup(
            title="Kingdom End",
            economies=[
                food_and_drugs.with_name("T1–T2: Boron Food & Drugs").with_single_recipe(["Boron"]).done(),
            ],
        ),
    ]
