import numpy as np


class Pile:

    _young_modules = {
        "concrete": 2.05 * 10**4,
        "steel": 2.05 * 10**5
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


def deformation(pile: Pile, div_size, div_num, force, khs, condition):
    """ 差分法によって変形を算出する """

    # 杭頭境界条件を設定
    k0 = np.inf if condition == "fix" else 1.0e-10

    # 式が見やすいように整理
    b, n, h, ei = float(pile.diameter), int(div_num), float(div_size), float(pile.stiffness)
    p = float(force) * 1e3
    # 事前計算（stiff = EI）
    c1s = 6 + h ** 4 * np.array(khs) * b / ei
    c2 = ei / k0
    c3 = -2 * p * h ** 3 / ei

    # 左辺のマトリクスを作成
    left = np.zeros((n + 5, n + 5))
    # 境界条件を入力
    left[0, 0:5] = [-1, 2, 0, -2, 1]
    left[1, 0:5] = [0, c2 - h, -2 * c2, c2 + h, 0]
    left[-1, -5:] = [-1, 2, 0, -2, 1]
    left[-2, -5:] = [0, 1, -2, 1, 0]
    # その他の行に一般式を入れ込んでいく
    for i in range(2, n + 3):
        left[i, i - 2:i + 3] = [1, -4, c1s[i - 2], -4, 1]

    # 右辺のマトリクスを作成
    right = np.zeros(n + 5)
    right[0] = c3

    # 連立方程式を解く
    ans = -np.linalg.solve(left, right)

    return ans
