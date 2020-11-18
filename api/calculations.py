from typing import Tuple

import numpy as np
import pandas as pd
from scipy import interpolate

_YOUNG_MODULES = {
    'concrete': 2.05e4,
    'steel': 2.05e5
}


class ExcelColumns:
    depth = '深度'
    nValue = 'N値'
    soil = '土質'
    reductions = '低減係数'
    adopted_reductions = '採用低減係数'
    alpha = 'alpha'
    E0 = 'E0'


def get_results(mode, condition, bottom_condition, material, diameter, length, level, force, soil_data, div_num) -> dict:

    diameter = float(diameter)  # mm
    length = float(length) * 1e3  # to mm
    level = float(level) * 1e3  # to mm
    force = float(force) * 1e3  # to N
    div_num = int(div_num)

    div_size = length / div_num
    x = np.linspace(-level, length - level, div_num + 1)

    kh0s = kh_by_soil_data(diameter, x, soil_data)
    stiffness = pile_stiffness(diameter, diameter, 0, material)

    k0 = top_condition_to_stiffness(mode, condition, bottom_condition, div_num, div_size, stiffness, diameter, kh0s, force)

    y, dec = solve_y(mode, bottom_condition, div_num, div_size, stiffness, diameter, kh0s, k0, force)
    t = np.gradient(y, div_size)  # solve degree
    m = -np.gradient(t, div_size) * stiffness  # solve moment
    q = np.gradient(m, div_size)  # solve shear

    q[2] = -force
    q[-3] = q[-4]

    format_for_chart = []
    for (x, dec, kh0s, y, t, m, q) in zip(x, dec, kh0s, y[2:-2], t[2:-2], m[2:-2], q[2:-2]):
        format_for_chart.append({"x": x / 1e3, "dec": dec, "kh0s": kh0s * 1e6, "y": y, "t": t * 1e3, "m": m / 1e6, "q": q / 1e3})

    return format_for_chart


def kh_by_soil_data(diameter: float, x: np.ndarray, soil_data: dict):

    depth = np.array(soil_data.get('depth')) * 1e3
    alpha = np.array(soil_data.get('alpha'))
    beta = np.array(soil_data.get('adopted_reductions'))
    E0 = np.array(soil_data.get('E0'))

    kh = alpha * beta * E0 * (diameter / 10) ** (-3 / 4)

    fitted = interpolate.interp1d(depth, kh)  # 線形補間
    fitted_kh = fitted(x)

    return fitted_kh / 1e6  # N/mm2


def top_condition_to_stiffness(mode, condition, bottom_condition, div_num, div_size, stiffness, diameter, kh0s, force) -> float:
    condition = float(condition)
    if condition == 1.0:
        k0 = np.inf
    elif condition == 0.0:
        k0 = 10e-15
    else:
        k0 = half_condition_solver(mode, bottom_condition, condition, div_num, div_size, stiffness, diameter, kh0s, force)
    return k0


def half_condition_solver(mode, bottom_condition, condition, div_num, div_size, stiffness, diameter, kh0s, force):
    y_at_fix, _ = solve_y(mode, bottom_condition, div_num, div_size, stiffness, diameter, kh0s, np.inf, force)
    y_at_pin, _ = solve_y(mode, bottom_condition, div_num, div_size, stiffness, diameter, kh0s, 10e-15, force)

    moment_at_fix = -np.gradient(np.gradient(y_at_fix, div_size), div_size)[2] * stiffness
    degree_at_pin = np.gradient(y_at_pin, div_size)[2]

    condition = float(condition)
    half_moment = moment_at_fix * condition
    half_degree = degree_at_pin * (1 - condition)

    k0 = half_moment / half_degree

    err = 1.1e6
    while err > 1.0e6:
        y, _ = solve_y(mode, bottom_condition, div_num, div_size, stiffness, diameter, kh0s, k0, force)
        m = -np.gradient(np.gradient(y, div_size), div_size)[2] * stiffness
        err = m - half_moment
        k0 = k0 * half_moment / m

    return k0


def pile_stiffness(diameter: float, thickness: float, thickness_margin: float, material: str) -> float:
    sec1 = np.pi * (diameter - thickness_margin * 2) ** 4 / 64
    sec2 = np.pi * (diameter - thickness) ** 4 / 64
    return (sec1 - sec2) * _YOUNG_MODULES.get(material)


def solve_y(mode, bottom_condition, div_num, div_size, stiffness, diameter, kh0s, k0, force):
    if mode == 'liner':
        y, dec = deformation_analysis_by_FDM(bottom_condition, div_num, div_size, stiffness, diameter, kh0s, k0, force)
    elif mode == 'non_liner_multi':
        y, dec = deformation_analysis_by_non_liner_FDM(bottom_condition, div_num, div_size, stiffness, diameter, kh0s, k0, force)
    elif mode == 'non_liner_single':
        y, dec = deformation_analysis_by_non_liner_single_FDM(bottom_condition, div_num, div_size, stiffness, diameter, kh0s, k0, force)
    else:
        y, dec = deformation_analysis_by_FDM(bottom_condition, div_num, div_size, stiffness, diameter, kh0s, k0, force)
    return y, dec


def deformation_analysis_by_FDM(bottom_condition, div_num: int, div_size: float, stiffness: float, diameter: float, khs: np.ndarray, k0: float, force: float) -> Tuple[np.ndarray, np.ndarray]:

    def _left_matrix(bottom_condition, n, h, ei, b, khs, k0):
        left = np.zeros((n + 5, n + 5))
        # head row
        left[0, 0:5] = [-1, 2, 0, -2, 1]
        left[1, 0:5] = [0, ei / k0 - h, -2 * ei / k0, ei / k0 + h, 0]
        # general row
        c1s = 6 + h ** 4 * khs * b / ei
        for i in range(2, n + 3):
            left[i, i - 2:i + 3] = [1, -4, c1s[i - 2], -4, 1]
        # tail row

        if bottom_condition == "free":
            left[-1, -5:] = [-1, 2, 0, -2, 1]
            left[-2, -5:] = [0, 1, -2, 1, 0]
        elif bottom_condition == "pin":
            left[-1, -5:] = [1, 0, 1, 0, 1]
            left[-2, -5:] = [0, 1, 1, 1, 0]
        else:
            left[-1, -5:] = [1, 0, 1, 0, 1]
            left[-2, -5:] = [0, 1, 1, 1, 0]

        return left

    def _right_matrix(n, h, ei, force):
        right = np.zeros(n + 5)
        right[0] = -2 * force * h ** 3 / ei
        return right

    left = _left_matrix(bottom_condition, div_num, div_size, stiffness, diameter, khs, k0)
    right = _right_matrix(div_num, div_size, stiffness, force)
    y = -np.linalg.solve(left, right)  # 連立方程式を解く
    dec = np.ones_like(y)  # 低減係数(線形計算の場合は1.0)
    return y, dec


def deformation_analysis_by_non_liner_FDM(bottom_condition, div_num: int, div_size: float, stiffness: float, diameter: float, khs: np.ndarray, k0: float, force: float) -> Tuple[np.ndarray, np.ndarray]:

    dec_khs = khs
    y, _ = deformation_analysis_by_FDM(bottom_condition, div_num, div_size, stiffness, diameter, khs, k0, force)  # 初期値

    err = np.ones_like(khs)
    dec = err

    while np.any(err > 0.1):
        dec = np.where(np.abs(y) > 10, (np.abs(y) / 10) ** (-1 / 2), 1.0)  # 地盤の非線形考慮
        dec_khs = khs * dec[2:-2]
        new_y, _ = deformation_analysis_by_FDM(bottom_condition, div_num, div_size, stiffness, diameter, dec_khs, k0, force)
        err = np.abs(new_y - y)
        y = new_y

    return y, dec


def deformation_analysis_by_non_liner_single_FDM(bottom_condition, div_num: int, div_size: float, stiffness: float, diameter: float, khs: np.ndarray, k0: float, force: float) -> Tuple[np.ndarray, np.ndarray]:

    dec_khs = khs
    y, _ = deformation_analysis_by_FDM(bottom_condition, div_num, div_size, stiffness, diameter, khs, k0, force)  # 初期値

    err = np.ones_like(khs)
    dec = err

    while np.any(err > 0.1):
        dec = np.where(np.abs(y) > 10, (np.abs(y) / 10) ** (-1 / 2), 1.0)[2] * np.ones_like(y)
        dec_khs = khs * dec[2:-2]
        new_y, _ = deformation_analysis_by_FDM(bottom_condition, div_num, div_size, stiffness, diameter, dec_khs, k0, force)
        err = np.abs(new_y - y)
        y = new_y

    return y, dec


def decode_upload_file(file):
    df = pd.read_excel(file)
    # df[ExcelColumns.reductions] = df[ExcelColumns.reductions].fillna(1.0)
    # df[ExcelColumns.adopted_reductions] = df[ExcelColumns.adopted_reductions].fillna(1.0)

    # formated_data = {}
    # for i, column in enumerate(df):
    #     for j, row in enumerate(df[column]):
    #         formated_data["{}-{}".format(j, i)] = str(row)
    # return {"data": formated_data, "row_num": len(df[ExcelColumns.depth])}

    return dict(
        depth=df[ExcelColumns.depth].values.tolist(),
        nValue=df[ExcelColumns.nValue].values.tolist(),
        soil=df[ExcelColumns.soil].values.tolist(),
        reductions=df[ExcelColumns.reductions].fillna(1.0).values.tolist(),
        adopted_reductions=df[ExcelColumns.adopted_reductions].fillna(1.0).values.tolist(),
        alpha=df[ExcelColumns.alpha].values.tolist(),
        E0=df[ExcelColumns.E0].values.tolist()
    )
