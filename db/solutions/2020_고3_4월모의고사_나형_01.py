import math

# 원래 식: 3 × 8^(1/3)
result = 3 * (8 ** (1/3))

# 정답값
candidate = 6

# 검증
if math.isclose(result, candidate, rel_tol=1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')