from sympy import symbols, expand, simplify

# 주어진 조건
sum_a = 8
sum_a_sq = 20

# 계산
result = sum_a_sq + 2 * sum_a - 3 * 8

# 검증
expected = 12
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')