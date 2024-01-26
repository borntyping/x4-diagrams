import typing

from x4.economy.economy import Economy
from x4_data.economy import TIER_3, TIER_4, TIER_5, TIER_6, WARES


def subsets() -> typing.Mapping[str, typing.Sequence[Economy]]:
    world = Economy("X4", WARES).done()
    universal = world.with_name("Universal").filter_by_method(["Universal"]).done()

    food_and_drugs = world.with_name("Tier 1–2: Food & Drugs").filter_by_tier({1, 2}).done()
    construction = universal.with_name("Tier 3–6: Construction").filter_by_tier({3, 4, 5, 6}).done()

    return {
        "Universal": [
            food_and_drugs.remove_common_inputs(),
            construction.remove_common_inputs(),
            food_and_drugs,
            construction,
            universal.with_name(str(TIER_3)).filter_by_tier({3}).done(),
            universal.with_name(str(TIER_4)).filter_by_tier({4}).done(),
            universal.with_name(str(TIER_5)).filter_by_tier({5}).done(),
            universal.with_name(str(TIER_6)).filter_by_tier({6}).done(),
        ],
        "Commonwealth": [
            world.with_name("Commonwealth Tier 1–2: Food & Drugs")
            .filter_by_tier({1, 2})
            .filter_by_method(["Universal", "Argon", "Boron", "Paranid", "Split", "Teladi"])
            .done(),
        ],
        "Argon": [world.with_name("Argon Food & Drugs").filter_by_method(["Argon"]).filter_by_tier({1, 2}).done()],
        "Boron": [world.with_name("Boron Food & Drugs").filter_by_method(["Boron"]).filter_by_tier({1, 2}).done()],
        "Paranid": [world.with_name("Paranid Food & Drugs").filter_by_method(["Paranid"]).filter_by_tier({1, 2}).done()],
        "Teladi": [
            world.with_name("Teladi Food & Drugs").filter_by_method(["Teladi"]).filter_by_tier({1, 2}).done(),
            world.with_name("Teladi Construction")
            .filter_by_method(["Teladi", "Universal"])
            .filter_by_tier({3, 4, 5, 6})
            .done(),
        ],
    }
