import math
from sympy import sin, cos, tan, pi, simplify, symbols

CANDIDATE = 48

# 주어진 조건에서 sin(θ) = -3/5
sin_theta = -3/5

# sin(π/2+θ) = cos(θ)
# tan(π-θ) = -tan(θ)
# cos²(θ) + sin²(θ) = 1이므로
cos_theta_sq = 1 - sin_theta**2
cos_theta_sq = 1 - (9/25)
cos_theta_sq = 16/25

# 주어진 식 검증: sin(π/2+θ)·tan(π-θ) = 3/5
# cos(θ) · (-tan(θ)) = -sin(θ) = -(-3/5) = 3/5 ✓

left_side = -sin_theta  # cos(θ) · (-sin(θ)/cos(θ)) = -sin(θ)
if abs(left_side - 3/5) < 1e-10:
    result = 30 * (1 - sin_theta)
    if abs(result - CANDIDATE) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')