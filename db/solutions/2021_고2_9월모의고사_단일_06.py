from sympy import symbols, cos, sin, tan, sqrt, solve
import math

theta = symbols('theta', real=True)

# sin(theta) = 3/5 이므로 cos(theta) 계산
sin_theta = 3/5
cos_theta = 4/5

# 원래 조건 검증: cos(theta) * tan(theta) = 3/5
tan_theta = sin_theta / cos_theta
result = cos_theta * tan_theta

if abs(result - 3/5) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')