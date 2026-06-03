import math

# 원래 벡터들
a = (4, 1)
b = (-2, 0)

# 합 계산
sum_vec = (a[0] + b[0], a[1] + b[1])

# 크기 계산
magnitude = math.sqrt(sum_vec[0]**2 + sum_vec[1]**2)

# 정답 검증
answer_value = math.sqrt(5)
if abs(magnitude - answer_value) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')