import pytest

from main import calculations as calc

single_layered_ground = calc.decode_upload_file('tests/single_layer.xlsx')


def test_single_layer_and_liner():

    kargs = {
        "mode": "liner",
        "condition": "1.0",
        "bottom_condition": "pin",
        "material": "steel",
        "diameter": "200",
        "length": "100",
        "level": "-1.15",
        "force": "200",
        "div_num": "500",
        "soil_data": single_layered_ground
    }

    results = calc.get_results(**kargs)

    # 入力条件の確認
    assert results['x'][0] == 1.15
    assert results['dec'][0] == 1.0
    assert results['kh0s'][0] == pytest.approx(17763.83723)

    # 単層地盤扱いとなっていることを確認
    assert len(set(results['dec'])) == 1
    assert len(set(results['kh0s'])) == 1

    # 杭頭 = 最大 の確認
    assert max(results['y']) == results['y'][0]
    assert max(results['m']) == results['m'][0]
    assert min(results['q']) == results['q'][0]

    # 杭脚 = 0 の確認
    assert results['y'][-1] == pytest.approx(0.0)
    assert results['m'][-1] == pytest.approx(0.0)
    assert results['q'][-1] == pytest.approx(0.0)

    # 杭頭の値の確認
    assert max(results['y']) == pytest.approx(27.557752, 0.01)
    assert max(results['m']) == pytest.approx(204.27698, 0.1)
    assert min(results['q']) == pytest.approx(-200.0)

    # 中央部の確認
    assert min(results['m']) == pytest.approx(-42.489612, 0.1)


def test_single_layer_and_non_liner():

    kargs = {
        "mode": "non_liner_single",
        "condition": "1.0",
        "bottom_condition": "pin",
        "material": "steel",
        "diameter": "200",
        "length": "100",
        "level": "-1.15",
        "force": "200",
        "div_num": "500",
        "soil_data": single_layered_ground
    }

    results = calc.get_results(**kargs)

    # 入力条件の確認
    assert results['x'][0] == 1.15
    assert results['dec'][0] == pytest.approx(0.444431, 0.01)
    assert results['kh0s'][0] == pytest.approx(17763.83723)

    # 単層地盤扱いとなっていることを確認
    assert len(set(results['dec'])) == 1
    assert len(set(results['kh0s'])) == 1

    # 杭頭 = 最大 の確認
    assert max(results['y']) == results['y'][0]
    assert max(results['m']) == results['m'][0]
    assert min(results['q']) == results['q'][0]

    # 杭脚 = 0 の確認
    assert results['y'][-1] == pytest.approx(0.0)
    assert results['m'][-1] == pytest.approx(0.0)
    assert results['q'][-1] == pytest.approx(0.0)

    # 杭頭の値の確認
    assert max(results['y']) == pytest.approx(50.627948, 0.1)
    assert max(results['m']) == pytest.approx(250.18904, 0.1)
    assert min(results['q']) == pytest.approx(-200.0)

    # 中央部の確認
    assert min(results['m']) == pytest.approx(-52.039320, 0.1)
