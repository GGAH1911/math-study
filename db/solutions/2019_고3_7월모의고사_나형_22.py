import math

CANDIDATE = 42

# $_7P_2$ 계산
n = 7
r = 2
result = math.factorial(n) // math.factorial(n - r)

# 직접 계산으로도 검증
direct_result = 7 * 6

if result == CANDIDATE and direct_result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')