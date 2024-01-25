import pytest

from x4.types import WareFilter


@pytest.mark.parametrize(
    ("wf", "key", "expected"),
    [
        (WareFilter(include={"a"}), "a", True),
        (WareFilter(include={"b"}), "a", False),
        (WareFilter(include={"a"}, exclude={"a"}), "a", False),
        (WareFilter(include={"b"}, exclude={"a"}), "a", False),
        (WareFilter(include={"helium"}), "helium", True),
    ],
)
def test_ware_filter(wf: WareFilter, key: str, expected: bool) -> None:
    assert wf.match(key) == expected
