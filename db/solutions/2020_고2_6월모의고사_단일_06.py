import math
from sympy import symbols, sin, cos, tan, sqrt, pi, solve

# 주어진 조건
theta = symbols('theta', real=True)
cos_theta = -4/5

# sin θ 구하기 (항등식)
sin_squared = 1 - cos_theta**2
sin_theta_abs = sqrt(sin_squared)

# 제3사분면 (π < θ < 3π/2)에서 sin θ < 0
sin_theta = -sin_theta_abs

# tan θ 계산
tan_theta = sin_theta / cos_theta
tan_theta_value = float(tan_theta)

# 검증
if abs(tan_theta_value - 0.75) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')