from typing import Tuple
import numpy as np
from scipy import interpolate

_YOUNG_MODULES = {
    'concrete': 2.05e4,
    'steel': 2.05e5
}


def get_results(mode, condition, bottom_condition, material, diameter, length, level, force, soil_data) -> dict:

    diameter = float(diameter)  # mm
    length = float(length) * 1e3  # to mm
    level = float(level) * 1e3  # to mm
    force = float(force) * 1e3  # to N

    div_num = 100
    div_size = length / div_num
    x = np.linspace(-level, length - level, div_num + 1)

    kh0s = kh_by_soil_data(diameter, x, soil_data)
    stiffness = pile_stiffness(diameter, diameter, 0, material)

    k0 = top_condition_to_stiffness(mode, condition, div_num, div_size, stiffness, diameter, kh0s, force)

    y, dec = solve_y(mode, div_num, div_size, stiffness, diameter, kh0s, k0, force)
    t = np.gradient(y, div_size)  # solve degree
    m = -np.gradient(t, div_size) * stiffness  # solve moment
    q = np.gradient(m, div_size)  # solve shear
    q[2] = -force

    return dict(
        x=x / 1e3,        # m
        dec=dec,
        kh0s=kh0s * 1e6,  # kN/m3 (低減前の地盤反力係数)
        y=y[2:-2],        # mm
        t=t[2:-2] * 1e3,  # x10^3 rad
        m=m[2:-2] / 1e6,  # kNm
        q=q[2:-2] / 1e3   # kN
    )


def kh_by_soil_data(diameter: float, x: np.ndarray, soil_data: dict):

    depth = np.array(soil_data.get('depth')) * 1e3
    alpha = np.array(soil_data.get('alpha'))
    beta = np.array(soil_data.get('adopted_reductions'))
    E0 = np.array(soil_data.get('E0'))

    kh = alpha * beta * E0 * (diameter / 10) ** (-3 / 4)

    fitted = interpolate.interp1d(depth, kh)  # 線形補間
    fitted_kh = fitted(x)

    return fitted_kh / 1e6  # N/mm2


def top_condition_to_stiffness(mode, condition, div_num, div_size, stiffness, diameter, kh0s, force) -> float:
    if condition == "1.0":
        k0 = np.inf
    elif condition == "0.0":
        k0 = 10e-15
    else:
        k0 = half_condition_solver(mode, condition, div_num, div_size, stiffness, diameter, kh0s, force)
    return k0


def half_condition_solver(mode, condition, div_num, div_size, stiffness, diameter, kh0s, force):
    y_at_fix, _ = solve_y(mode, div_num, div_size, stiffness, diameter, kh0s, np.inf, force)
    y_at_pin, _ = solve_y(mode, div_num, div_size, stiffness, diameter, kh0s, 10e-15, force)

    moment_at_fix = -np.gradient(np.gradient(y_at_fix, div_size), div_size)[2] * stiffness
    degree_at_pin = np.gradient(y_at_pin, div_size)[2]

    condition = float(condition)
    half_moment = moment_at_fix * condition
    half_degree = degree_at_pin * (1 - condition)

    k0 = half_moment / half_degree

    err = 1.1e6
    while err > 1.0e6:
        y, _ = solve_y(mode, div_num, div_size, stiffness, diameter, kh0s, k0, force)
        m = -np.gradient(np.gradient(y, div_size), div_size)[2] * stiffness
        err = m - half_moment
        k0 = k0 * half_moment / m

    return k0


def pile_stiffness(diameter: float, thickness: float, thickness_margin: float, material: str) -> float:
    sec1 = np.pi * (diameter - thickness_margin * 2) ** 4 / 64
    sec2 = np.pi * (diameter - thickness) ** 4 / 64
    return (sec1 - sec2) * _YOUNG_MODULES.get(material)


def solve_y(mode, div_num, div_size, stiffness, diameter, kh0s, k0, force):
    if mode == 'liner':
        y, dec = deformation_analysis_by_FDM(div_num, div_size, stiffness, diameter, kh0s, k0, force)
    elif mode == 'non_liner':
        y, dec = deformation_analysis_by_non_liner_FDM(div_num, div_size, stiffness, diameter, kh0s, k0, force)
    elif mode == 'non_liner_single':
        y, dec = deformation_analysis_by_non_liner_single_FDM(div_num, div_size, stiffness, diameter, kh0s, k0, force)
    else:
        y, dec = deformation_analysis_by_FDM(div_num, div_size, stiffness, diameter, kh0s, k0, force)
    return y, dec


def deformation_analysis_by_FDM(div_num: int, div_size: float, stiffness: float, diameter: float, khs: np.ndarray, k0: float, force: float) -> Tuple[np.ndarray, np.ndarray]:

    def _left_matrix(n, h, ei, b, khs, k0):
        left = np.zeros((n + 5, n + 5))
        # head row
        left[0, 0:5] = [-1, 2, 0, -2, 1]
        left[1, 0:5] = [0, ei / k0 - h, -2 * ei / k0, ei / k0 + h, 0]
        # general row
        c1s = 6 + h ** 4 * khs * b / ei
        for i in range(2, n + 3):
            left[i, i - 2:i + 3] = [1, -4, c1s[i - 2], -4, 1]
        # tail row
        left[-1, -5:] = [-1, 2, 0, -2, 1]
        left[-2, -5:] = [0, 1, -2, 1, 0]
        return left

    def _right_matrix(n, h, ei, force):
        right = np.zeros(n + 5)
        right[0] = -2 * force * h ** 3 / ei
        return right

    left = _left_matrix(div_num, div_size, stiffness, diameter, khs, k0)
    right = _right_matrix(div_num, div_size, stiffness, force)
    y = -np.linalg.solve(left, right)  # 連立方程式を解く
    dec = np.ones_like(y)  # 低減係数(線形計算の場合は1.0)
    return y, dec


def deformation_analysis_by_non_liner_FDM(div_num: int, div_size: float, stiffness: float, diameter: float, khs: np.ndarray, k0: float, force: float) -> Tuple[np.ndarray, np.ndarray]:

    dec_khs = khs
    y, _ = deformation_analysis_by_FDM(div_num, div_size, stiffness, diameter, khs, k0, force)  # 初期値

    err = np.ones_like(khs)
    dec = err

    while np.any(err > 0.1):
        dec = np.where(np.abs(y) > 10, (np.abs(y) / 10) ** (-1 / 2), 1.0)  # 地盤の非線形考慮
        dec_khs = khs * dec[2:-2]
        new_y, _ = deformation_analysis_by_FDM(div_num, div_size, stiffness, diameter, dec_khs, k0, force)
        err = np.abs(new_y - y)
        y = new_y

    return y, dec


def deformation_analysis_by_non_liner_single_FDM(div_num: int, div_size: float, stiffness: float, diameter: float, khs: np.ndarray, k0: float, force: float) -> Tuple[np.ndarray, np.ndarray]:

    dec_khs = khs
    y, _ = deformation_analysis_by_FDM(div_num, div_size, stiffness, diameter, khs, k0, force)  # 初期値

    err = np.ones_like(khs)
    dec = err

    while np.any(err > 0.1):
        dec = np.where(np.abs(y) > 10, (np.abs(y) / 10) ** (-1 / 2), 1.0)[2] * np.ones_like(y)
        dec_khs = khs * dec[2:-2]
        new_y, _ = deformation_analysis_by_FDM(div_num, div_size, stiffness, diameter, dec_khs, k0, force)
        err = np.abs(new_y - y)
        y = new_y

    return y, dec
