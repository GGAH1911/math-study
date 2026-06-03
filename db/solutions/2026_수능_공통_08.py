import sympy as sp
from sympy import sin, cos, pi, sqrt, simplify

theta = sp.Symbol('theta', real=True)
sin_theta = 3*sqrt(10)/10
cos_theta = -sqrt(10)/10

# 조건 1: sin(theta) + 3*cos(theta) = 0
cond1 = sin_theta + 3*cos_theta
result1 = simplify(cond1)

# 조건 2: cos(pi - theta) > 0
cond2_val = -cos_theta

# 기본 항등식
cond3 = sin_theta**2 + cos_theta**2
result3 = simplify(cond3)

if result1 == 0 and cond2_val > 0 and result3 == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')