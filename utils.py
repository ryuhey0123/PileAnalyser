import numpy as np


def deformation(diameter, div_size, div_num, force, stiff, khs, condition):
    k0 = np.inf if condition == "fix" else 1.0e-10
    # 式が見やすいように整理
    b, n, h, ei = float(diameter), int(div_num), float(div_size), float(stiff)
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

    return -np.linalg.solve(left, right)


def deformation_by_non_liner(diameter, div_size, div_num, force, stiff, kh0s, condition, dec_mode):
    err = np.ones(int(div_num) + 5) * 10
    y = deformation(diameter, div_size, div_num, force, stiff, kh0s, condition)
    while np.any(err > 0.1):
        y0 = y
        khs_dec = reduced_khs(y, kh0s, dec_mode)
        y = deformation(diameter, div_size, div_num, force, stiff, khs_dec, condition)
        err = abs(y - y0)
    return y


def reduced_khs(y, kh0s, dec_mode):
    y = np.array(y)
    kh0s = np.array(kh0s)
    if dec_mode == 'multi':
        dec = np.where(abs(y) > 10, (abs(y) / 10)**(-1/2), 1.0)[2:-2]
    else:
        dec = (abs(y[2]) / 10)**(-1/2) if abs(y[2]) > 10 else 1.0
    return kh0s * dec


def theta(y, h):
    return np.gradient(np.array(y), float(h))


def moment(t, h, stiff):
    return - np.gradient(np.array(t), float(h)) * float(stiff)


def shear(m, h, q0):
    q = np.gradient(np.array(m), float(h))
    q[2] = -float(q0) * 1e3
    return q