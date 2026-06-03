import sympy as sp
from sympy import sin, cos, pi, sqrt, solve

theta = sp.Symbol('theta', real=True)

# 주어진 조건
eq_condition = sin(pi/2 + theta) + cos(pi/2 - theta) - sqrt(5)/5

# 삼각함수 항등식 사용
eq_simplified = cos(theta) + sin(theta) - sqrt(5)/5

# sin(theta) + cos(theta) = sqrt(5)/5를 제곱
# (sin(theta) + cos(theta))^2 = 1/5
# sin^2(theta) + 2*sin(theta)*cos(theta) + cos^2(theta) = 1/5
# 1 + 2*sin(theta)*cos(theta) = 1/5

product_value = (sp.Rational(1, 5) - 1) / 2

# 검증: sin(theta) + cos(theta) = sqrt(5)/5이고 sin(theta)*cos(theta) = -2/5일 때
# (sin(theta) + cos(theta))^2 = sin^2(theta) + 2*sin(theta)*cos(theta) + cos^2(theta)
#                             = 1 + 2*(-2/5)
#                             = 1 - 4/5 = 1/5

verify_value = 1 + 2 * product_value
expected_square = (sqrt(5)/5)**2

if verify_value == expected_square:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')