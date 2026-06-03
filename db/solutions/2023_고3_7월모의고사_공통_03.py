import numpy as np
from sympy import *

# 주어진 조건
# sin(π/2 + θ) = 3/5
# 이는 cos(θ) = 3/5
cos_theta = Rational(3, 5)

# sin²θ + cos²θ = 1에서 sin²θ 계산
sin_sq = 1 - cos_theta**2
sin_sq_value = simplify(sin_sq)

# sin θ = ±4/5
sin_theta_pos = sqrt(sin_sq_value)
sin_theta_neg = -sqrt(sin_sq_value)

# 조건: sin(θ)cos(θ) < 0 확인
cond_pos = sin_theta_pos * cos_theta
cond_neg = sin_theta_neg * cos_theta

# 조건을 만족하는 sin(θ) 선택
if float(cond_neg) < 0:
    sin_theta = sin_theta_neg
else:
    sin_theta = sin_theta_pos

# 답 계산
answer = sin_theta + 2 * cos_theta
answer_simplified = simplify(answer)

# 검증
verify_identity = (sin_theta**2 + cos_theta**2)
verify_condition = sin_theta * cos_theta

if verify_identity == 1 and verify_condition < 0 and answer_simplified == Rational(2, 5):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')