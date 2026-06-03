from sympy import binomial
import math

# $_4H_3$ 계산: nHr = C(n+r-1, r)
n, r = 4, 3
result = binomial(n + r - 1, r)

# 직접 계산으로 검증
direct = math.comb(6, 3)

if result == 20 and direct == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')