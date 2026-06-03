import math

# 원래 문제식에서 주어진 값들
sqrt_2 = math.sqrt(2)

# 계산: 5^(sqrt(2)+1) × (1/5)^sqrt(2)
term1 = 5 ** (sqrt_2 + 1)
term2 = (1/5) ** sqrt_2
result = term1 * term2

# 예상 답: 5
expected = 5

# 검증 (부동소수점 오차 고려)
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed {result}, expected {expected}')