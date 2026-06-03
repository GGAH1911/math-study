import math

# 주어진 조건: cos(π + θ) = 2√5/5
cos_pi_plus_theta = 2 * math.sqrt(5) / 5

# cos(π + θ) = -cos(θ)
cos_theta = -cos_pi_plus_theta

# sin²θ + cos²θ = 1
sin_theta_squared = 1 - cos_theta**2
sin_theta = math.sqrt(sin_theta_squared)  # 제2사분면이므로 양수

# 답 계산
answer = sin_theta + cos_theta
expected = -math.sqrt(5) / 5

if abs(answer - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')