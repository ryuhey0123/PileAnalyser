import pytest

from main import calculations as calc

single_layered_ground = calc.decode_upload_file('tests/single_layer.xlsx')


def test_single_layer_and_liner_x():

    kargs = {
        "mode": "liner",
        "condition": "1.0",
        "bottom_condition": "pin",
        "material": "steel",
        "diameter": "200",
        "length": "15",
        "level": "-1.15",
        "force": "200",
        "soil_data": single_layered_ground
    }

    results = calc.get_results(**kargs)

    assert results['x'][0] == 1.15
    assert results['dec'][0] == 1.0
    assert results['kh0s'][0] == pytest.approx(17763.83723)
    assert results['y'][0] == pytest.approx(27.557752, 0.01)
    assert results['m'][0] == pytest.approx(204.27698, 0.1)
    assert results['q'][0] == pytest.approx(-200.0)
