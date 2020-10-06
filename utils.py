from functools import wraps
import time

import numpy as np
from numba import jit


def stop_watch(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        start = time.time()
        result = func(*args,**kargs)
        elapsed_time = time.time() - start
        print(f"{func.__name__}は{elapsed_time:.5e}秒かかりました")
        return result
    return wrapper


class Pile:
    _young_modules = {
        "concrete": 2.05 * 10 ** 4,
        "steel": 2.05 * 10 ** 5
    }

    def __init__(self, material, diameter, thickness, thickness_margin=0.0):
        self.material = material
        self.diameter = diameter
        self.thickness = thickness
        self.thickness_margin = thickness_margin

        self.I = self.sectional_2nd_moment()
        self.E = self._young_modules[material]

        self.stiffness = self.I * self.E

    def sectional_2nd_moment(self):
        sec1 = np.pi * (self.diameter - self.thickness_margin * 2) ** 4 / 64
        sec2 = np.pi * (self.diameter - self.thickness) ** 4 / 64
        return sec1 - sec2


def deformation_analysis_by_FDM(diameter, div_size, div_num, force, stiffness, khs, condition):
    """ 差分法によって変形を算出する """

    # 杭頭境界条件を設定
    k0 = np.inf if condition == "fix" else 10e-10

    # 式が見やすいように整理
    b, n, h, ei = float(diameter), int(div_num), float(div_size), float(
        stiffness)

    left = _left_matrix(n, h, ei, k0, khs, b)  # 左辺のマトリクスを作成
    right = _right_matrix(n, force, h, ei)  # 右辺のマトリクスを作成
    ans = _linalg_solve(left, right)  # 連立方程式を解く

    return ans


@stop_watch
@jit
def deformation_analysis_by_FDM_converge(diameter, div_size, div_num, force, stiff, kh0s, condition, mode, dec_mode):
    err = np.ones(int(div_num) + 5) * 10
    y = deformation_analysis_by_FDM(diameter, div_size, div_num, force, stiff, kh0s, condition)
    while np.any(err > 0.1):
        y0 = y
        dec = reduced(y, mode, dec_mode)
        khs_dec = kh0s * dec
        y = deformation_analysis_by_FDM(diameter, div_size, div_num, force, stiff, khs_dec, condition)
        err = abs(y - y0)
    return y


def reduced(y, mode, dec_mode):
    y = np.array(y)
    if mode == 'liner':
        dec = np.ones_like(y)[2:-2]
    else:
        if dec_mode == 'multi':
            dec = np.where(abs(y) > 10, (abs(y) / 10)**(-1/2), 1.0)[2:-2]
        else:
            dec = np.ones_like(y)[2:-2]
            dec = dec * (abs(y[2]) / 10)**(-1/2) if abs(y[2]) > 10 else 1.0
    return dec


def _left_matrix(n, h, ei, k0, khs, b):
    left = np.zeros((n + 5, n + 5))
    left = _left_matrix_add_head_row(left, h, ei, k0)
    c1s = 6 + h ** 4 * np.array(khs) * b / ei
    left = _left_matrix_add_general_row(left, n, c1s)
    left = _left_matrix_add_tail_row(left)
    return left


def _right_matrix(n, force, h, ei):
    right = np.zeros(n + 5)
    right[0] = -2 * float(force) * 1e3 * h ** 3 / ei
    return right


@jit
def _left_matrix_add_head_row(left, h, ei, k0):
    c2 = ei / k0
    left[0, 0:5] = [-1, 2, 0, -2, 1]
    left[1, 0:5] = [0, c2 - h, -2 * c2, c2 + h, 0]
    return left


@jit
def _left_matrix_add_general_row(left, n, c1s):
    for i in range(2, n + 3):
        left[i, i - 2:i + 3] = [1, -4, c1s[i - 2], -4, 1]
    return left


@jit
def _left_matrix_add_tail_row(left):
    left[-1, -5:] = [-1, 2, 0, -2, 1]
    left[-2, -5:] = [0, 1, -2, 1, 0]
    return left


@jit
def _linalg_solve(left, right):
    ans = -np.linalg.solve(left, right)
    return ans
