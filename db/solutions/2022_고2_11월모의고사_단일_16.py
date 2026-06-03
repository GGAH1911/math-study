import sympy as sp
from sympy import sin, cos, pi, sqrt, simplify, Eq

theta = sp.Symbol('theta', real=True)

# 주어진 조건: 3*sin^2(theta + 2pi/3) = 8*sin(theta + pi/6)
sin_theta_pi6 = sp.Rational(1, 3)

# 검증: sin(theta + pi/6) = 1/3일 때 조건식이 만족되는지 확인
# sin(theta + 2pi/3) = cos(theta + pi/6)
cos_theta_pi6_squared = 1 - sin_theta_pi6**2
LHS = 3 * cos_theta_pi6_squared
RHS = 8 * sin_theta_pi6

if simplify(LHS - RHS) == 0:
    # cos(theta - pi/3) 계산
    # cos(theta - pi/3) = cos((theta + pi/6) - pi/2) = sin(theta + pi/6)
    result = sin_theta_pi6
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')