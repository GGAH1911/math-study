import math

# 원래 식: sqrt(20) + sqrt(5)
original = math.sqrt(20) + math.sqrt(5)

# 정답: 3*sqrt(5)
answer = 3 * math.sqrt(5)

# 검증
if abs(original - answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')