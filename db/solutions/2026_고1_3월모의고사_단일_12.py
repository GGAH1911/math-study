import math
from fractions import Fraction

# 계산된 중심각 (도)
alpha = 60   # arc AB
beta  = 80   # arc BC
gamma = 60   # arc CD
delta = 160  # arc DA
r = 5

try:
    # 전체 합
    assert alpha + beta + gamma + delta == 360, f'sum={alpha+beta+gamma+delta}'

    # AD || BC: arc AB == arc CD
    assert alpha == gamma, f'alpha={alpha}, gamma={gamma}'

    # inscribed angle DCB = 110 deg
    arc_DB_no_C = delta + alpha  # D->A->B
    angle_DCB = arc_DB_no_C / 2
    assert abs(angle_DCB - 110) < 1e-9, f'angle_DCB={angle_DCB}'

    # arc BC : arc CD = 4:3
    assert Fraction(beta, gamma) == Fraction(4, 3), f'ratio={Fraction(beta,gamma)}'

    # 호 DA (B 불포함) 길이
    arc_DA_rad = delta * math.pi / 180
    arc_DA_len = r * arc_DA_rad
    expected = 40 * math.pi / 9

    assert abs(arc_DA_len - expected) < 1e-9, f'arc_DA={arc_DA_len}, expected={expected}'

    print('VERIFY_PASS')
except AssertionError as e:
    print(f'VERIFY_FAIL: {e}')
