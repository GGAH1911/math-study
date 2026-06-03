import math

# 원래 식: 4^(1/4) × 2^(1/2)
result = (4 ** (1/4)) * (2 ** (1/2))

# 예상 답: 2
expected = 2

# 검증
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')