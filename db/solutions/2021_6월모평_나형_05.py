import sympy as sp
from sympy import sin, cos, pi, sqrt, symbols, solve

# 정현법칙 검증
R = 15  # 외접원의 반지름
sin_B = sp.Rational(7, 10)
AC = 21

# 정현법칙: AC / sin(B) = 2R
ratio = AC / sin_B
expected_2R = 2 * R

if ratio == expected_2R:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {ratio} != {expected_2R}')