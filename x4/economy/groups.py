import dataclasses
import typing

from x4.economy.economy import Economy
from x4.types import Method
from x4_data.economy import TIER_3, TIER_4, TIER_5, TIER_6, WARES


@dataclasses.dataclass(frozen=True)
class EconomyGroup:
    title: str
    economies: typing.Sequence[Economy]


def groups() -> typing.Sequence[EconomyGroup]:
    world = Economy("X4", WARES).done()
    universal = world.with_name("Universal").filter_by_method(["Universal"]).done()

    food_and_drugs = world.with_name("T1–T2: Food & Drugs").filter_by_tier({1, 2}).done()
    construction = universal.with_name("T3–T6: Construction").filter_by_tier({3, 4, 5, 6}).done()
    commonwealth: list[Method] = ["Universal", "Argon", "Boron", "Paranid", "Split", "Teladi"]

    return [
        EconomyGroup(
            title="Universal",
            economies=[
                food_and_drugs,
                construction,
                universal.with_name(str(TIER_3)).filter_by_tier({3}).done(),
                universal.with_name(str(TIER_4)).filter_by_tier({4}).done(),
                universal.with_name(str(TIER_5)).filter_by_tier({5}).done(),
                universal.with_name(str(TIER_6)).filter_by_tier({6}).done(),
            ],
        ),
        EconomyGroup(
            title="Foundations",
            economies=[
                food_and_drugs.with_name("T1–T2: Commonwealth Food & Drugs").filter_by_method(commonwealth).done(),
                food_and_drugs.with_name("T1–T2: Argon Food & Drugs").filter_by_method(["Argon"]).done(),
                food_and_drugs.with_name("T1–T2: Boron Food & Drugs").filter_by_method(["Boron"]).done(),
                food_and_drugs.with_name("T1–T2: Paranid Food & Drugs").filter_by_method(["Paranid"]).done(),
                food_and_drugs.with_name("T1–T2: Teladi Food & Drugs").filter_by_method(["Teladi"]).done(),
                construction.with_name("T3–T6: Teladi Construction").filter_by_method(["Teladi", "Universal"]).done(),
            ],
        ),
        EconomyGroup(
            title="Split Vendetta",
            economies=[
                food_and_drugs.with_name("T1–T2: Split Food & Drugs").filter_by_method(["Split"]).done(),
            ],
        ),
        EconomyGroup(
            title="Cradle of Humanity",
            economies=[
                food_and_drugs.with_name("T1–T2: Terran Food & Drugs").filter_by_method(["Terran"]).done(),
                construction.with_name("T3–T6: Terran Construction").filter_by_method(["Terran"]).done(),
            ],
        ),
        EconomyGroup(
            title="Tides of Avarice",
            economies=[
                construction.with_name("T3–T6: Scrapping Construction").filter_by_method(["Recycling"]).done(),
                construction.with_name("T3–T6: Scrapping Construction").filter_by_method(["Recycling", "Universal"]).done(),
            ],
        ),
        EconomyGroup(
            title="Kingdom End",
            economies=[
                food_and_drugs.with_name("T1–T2: Boron Food & Drugs").filter_by_method(["Boron"]).done(),
            ],
        ),
    ]
