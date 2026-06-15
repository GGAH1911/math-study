import sympy as sp
from sympy import sqrt, symbols, solve

a_sq = 15
c_sq = 10
a_val = sqrt(15)
c_val = sqrt(10)

# 삼각형 AFF'의 꼭짓점
A = (a_val, 0)
F = (0, c_val)
F_prime = (0, -c_val)

# 넓이 = 1/2 * 밑변 * 높이
# F와 F'이 y축 위에 있으므로 밑변 = 2c, 높이 = a
area = sp.Rational(1, 2) * 2 * c_val * a_val
area_simplified = sp.simplify(area)
expected = 5 * sqrt(6)

if sp.simplify(area_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')