import math

# 방향벡터 정의
v1 = (4, 3)
v2 = (1, -3)

# 내적 계산
dot_product = v1[0] * v2[0] + v1[1] * v2[1]

# 크기 계산
mag_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
mag_v2 = math.sqrt(v2[0]**2 + v2[1]**2)

# cos theta 계산 (절댓값 사용)
cos_theta = abs(dot_product) / (mag_v1 * mag_v2)

# 예상 답: sqrt(10)/10
expected = math.sqrt(10) / 10

# 검증
if abs(cos_theta - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')