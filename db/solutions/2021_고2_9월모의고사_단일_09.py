import numpy as np
from sympy import sin, pi, symbols, simplify, solve

theta = symbols('theta', real=True)

# 삼각형 넓이 = 2*sin(theta)
area = 2 * sin(theta)

# 넓이 > 1 조건을 확인
# sin(theta) > 1/2
# 0 < theta < pi 범위에서 해는 pi/6 < theta < 5*pi/6

alpha = pi / 6
beta = 5 * pi / 6

# 경계점 확인
area_at_alpha = float(2 * sin(float(alpha)))
area_at_beta = float(2 * sin(float(beta)))

# alpha와 beta에서 넓이 = 1인지 확인
assert abs(area_at_alpha - 1.0) < 1e-10, f"alpha에서 넓이 = {area_at_alpha}, 1이어야 함"
assert abs(area_at_beta - 1.0) < 1e-10, f"beta에서 넓이 = {area_at_beta}, 1이어야 함"

# alpha < theta < beta 범위에서 넓이 > 1인지 샘플링으로 확인
test_theta = float((alpha + beta) / 2)  # pi/3
area_mid = 2 * np.sin(test_theta)
assert area_mid > 1.0, f"중간값에서 넓이 = {area_mid}, 1보다 커야 함"

# 최종 답: 2*alpha + beta
result = 2 * alpha + beta
result_simplified = simplify(result)
expected = 7 * pi / 6

assert simplify(result_simplified - expected) == 0, f"답 = {result_simplified}, 7π/6이어야 함"

print('VERIFY_PASS')