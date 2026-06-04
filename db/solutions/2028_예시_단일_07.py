import sympy as sp
from sympy import pi, simplify

# 부채꼴의 넓이 공식: A = (1/2) * r^2 * theta
r = 8
theta = 3*pi/4

# 넓이 계산
area = sp.Rational(1, 2) * r**2 * theta
area_simplified = simplify(area)

# 검증
expected_answer = 24*pi

if simplify(area_simplified - expected_answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')