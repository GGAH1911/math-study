import sympy as sp
from sympy import sin, cos, tan, pi, simplify, sqrt

# 주어진 조건: sin(3π/2 + θ) = 1/3
# 삼각함수 공식으로부터 cos(θ) = -1/3
cos_theta = -1/3
sin_squared_theta = 1 - cos_theta**2

# sin(θ)tan(θ) = sin²(θ)/cos(θ) 계산
result = sin_squared_theta / cos_theta

# 답: -8/3
expected_answer = -8/3

if abs(result - expected_answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')