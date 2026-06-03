import sympy as sp
from sympy import limit, oo, simplify

n = sp.Symbol('n', integer=True, positive=True)

# a_n의 극한값 계산
a_n_expr = (2**(n+1)) / (2**n + 1)
a_n_limit = limit(a_n_expr, n, oo)

# 구하는 극한
numerator = 2**n * a_n_limit + 5 * 2**(n+1)
denominator = 2**n + 3

# 큰 n에 대해 근사
result = limit(numerator / denominator, n, oo)

if result == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')