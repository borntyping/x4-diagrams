import pytest

from x4.types import Include


@pytest.mark.parametrize(
    ("wf", "key", "expected"),
    [
        (Include(include={"a"}), "a", True),
        (Include(include={"b"}), "a", False),
        (Include(include={"a"}, exclude={"a"}), "a", False),
        (Include(include={"b"}, exclude={"a"}), "a", False),
        (Include(include={"helium"}), "helium", True),
    ],
)
def test_ware_filter(wf: Include, key: str, expected: bool) -> None:
    assert wf.match(key) == expected
