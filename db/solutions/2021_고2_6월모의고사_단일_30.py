import numpy as np
from scipy.optimize import fsolve

# 조건 확인: a=14, b=13, sin(πt)=-6/7
a, b = 14, 13
sin_pi_t = -6/7
cos_sq_pi_t = 1 - sin_pi_t**2

# 식 검증: cos²(πt) = 13/49
expected_cos_sq = 13/49
assert abs(cos_sq_pi_t - expected_cos_sq) < 1e-10

# 답 검증
answer = (a * b) / cos_sq_pi_t
expected_answer = 686
assert abs(answer - expected_answer) < 1e-10

# x들의 합이 56인지 확인
# cos(π(14x+13)) = 1일 때, u = 2k, 13≤2k≤69
sum_u = sum(2*k for k in range(7, 35))  # k=7,...,34
sum_x = (sum_u - 13*28) / 14
assert abs(sum_x - 56) < 1e-10

print('VERIFY_PASS')