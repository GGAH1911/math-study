import math

# sin(x) = 2/3인 두 점 찾기
alpha = math.asin(2/3)
beta = math.pi - alpha

# 검증: 경계점에서 3*sin(x) - 2 = 0
assert abs(3*math.sin(alpha) - 2) < 1e-10
assert abs(3*math.sin(beta) - 2) < 1e-10

# 내부점에서 3*sin(x) - 2 > 0 확인
test_x = (alpha + beta) / 2
assert 3*math.sin(test_x) - 2 > 0

# cos(alpha + beta) 계산
result = math.cos(alpha + beta)

# 최종 답 검증
if abs(result - (-1)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')