import pytest

from x4.economy.economy import Economy


@pytest.mark.parametrize(
    ("name", "tiers"),
    [
        ["t1-t2", {1, 2}],
        ["t3-t6", {3, 4, 5, 6}],
    ],
)
def test_select_tiers(name: str, tiers: set[int]) -> None:
    Economy(name=name).select_tiers(tiers).verify()
