import math
from math import sqrt, pi

# 주어진 조건
sin_theta = sqrt(21) / 7

# 각도 θ는 π/2 < θ < π (제2사분면)
# sin(θ) = √21/7 일 때, cos²(θ) = 1 - sin²(θ)
cos_squared = 1 - (sin_theta ** 2)
cos_theta = -sqrt(cos_squared)  # 제2사분면에서 cos < 0

# tan(θ) 계산
tan_theta = sin_theta / cos_theta

# 정답 값
expected_answer = -sqrt(3) / 2

# 검증
if abs(tan_theta - expected_answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')