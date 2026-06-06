import sympy as sp
from sympy import sqrt, pi, cos, sin, symbols, Eq, solve

# 삼각형의 변의 길이 (CA = 7)
CA = 7
AB = 7 * sqrt(2) / 2
BC = 7 * sqrt(2)

# 외접원의 반지름 검증
# 코사인 법칙: cos C = (BC^2 + CA^2 - AB^2) / (2*BC*CA)
cos_C = (BC**2 + CA**2 - AB**2) / (2*BC*CA)
sin_C = sqrt(1 - cos_C**2)

# 사인 법칙: AB/sin(C) = 2R
two_R = AB / sin_C
R = two_R / 2

# 외접원의 넓이
area_circle = pi * R**2
expected_area = 28 * pi

# 검증: 넓이가 28π인지 확인
if sp.simplify(area_circle - expected_area) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')