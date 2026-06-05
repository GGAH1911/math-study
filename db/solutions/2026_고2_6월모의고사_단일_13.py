import sympy as sp
from sympy import pi, sqrt, cos, sin

# cos(B+C) = cos A + 1/2
# A + B + C = pi 이므로 B + C = pi - A
# cos(pi - A) = -cos A
# -cos A = cos A + 1/2
# -2 cos A = 1/2
# cos A = -1/4

cos_A = sp.Rational(-1, 4)
sin_A = sqrt(1 - cos_A**2)
sin_A_simplified = sqrt(sp.Rational(15, 16))
sin_A_val = sqrt(15) / 4

BC = 3

# 정현법칙: BC / sin A = 2R
two_R = BC / sin_A_val
R = two_R / 2
R_simplified = 2 * sqrt(15) / 5

# 외접원의 넓이
area = pi * R_simplified**2
area_simplified = sp.simplify(area)

# 기댓값
expected = 12 * pi / 5

# 검증
if sp.simplify(area_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')