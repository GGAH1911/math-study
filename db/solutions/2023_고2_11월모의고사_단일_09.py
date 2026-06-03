import sympy as sp
from sympy import sin, cos, tan, pi, solve, simplify

theta = sp.Symbol('theta', real=True)
sin2_theta = sp.Rational(2, 3)

# 원래 조건을 만족하는지 확인
# 2*sin(pi/2 - theta) = sin(theta) * tan(pi + theta)

lhs = 2 * sin(pi/2 - theta)
rhs = sin(theta) * tan(pi + theta)

# sin^2(theta) = 2/3일 때
# sin(theta) = ±sqrt(2/3), cos(theta) = ±sqrt(1/3)
# cos(theta)가 0이 아니어야 하므로 sin^2(theta) = 2/3, cos^2(theta) = 1/3

cos_theta = sp.sqrt(sp.Rational(1, 3))  # 양수로 가정
sin_theta = sp.sqrt(sp.Rational(2, 3))

theta_val = sp.atan2(sin_theta, cos_theta)

lhs_val = 2 * cos_theta
rhs_val = sin_theta * sin_theta / cos_theta
rhs_val = simplify(rhs_val)

if simplify(lhs_val - rhs_val) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')