from x4.economy.economy import Economy
from x4_data.economy import COMMONWEALTH


def test_filter_methods():
    e = Economy()
    e = e.done()
    e = e.filter_method(COMMONWEALTH)

    assert "protein_paste" not in e.wares_as_dict()
    assert "terran_mre" not in e.wares_as_dict()

    assert "wheat" in e.wares_as_dict()
    assert "medical_supplies" in e.wares_as_dict()
