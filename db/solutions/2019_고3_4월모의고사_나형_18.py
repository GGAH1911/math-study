import sympy as sp
from sympy import sqrt, pi, simplify

# 초기 삼각형 넓이
triangle_area = 16*sqrt(3)/3

# 초기 원의 넓이 (반원만 삼각형 내부)
circle_area_in_triangle = 2*pi

# 첫 단계
S1 = triangle_area - circle_area_in_triangle

# 무한급수: (a)(1 + r + r^2 + ...) = a/(1-r)
# 여기서 a = S1, r = 1/4
total = S1 / (1 - sp.Rational(1,4))
total = simplify(total)

expected = 64*sqrt(3)/9 - 8*pi/3
expected = simplify(expected)

if simplify(total - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')