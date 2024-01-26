from x4.types import Economy
from x4_data.economy import COMMONWEALTH, TIERS


def test_filter_methods():
    e = Economy(TIERS)
    e = e.validate()
    e = e.select_method(COMMONWEALTH)

    assert "protein_paste" not in e.wares()
    assert "terran_mre" not in e.wares()

    assert "wheat" in e.wares()
    assert "medical_supplies" in e.wares()
