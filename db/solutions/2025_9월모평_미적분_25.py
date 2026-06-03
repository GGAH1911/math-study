import sympy as sp
from sympy import limit, oo, simplify

n = sp.Symbol('n', integer=True, positive=True)
a1 = 3
r = sp.Rational(1, 2)

# 등비수열
an = a1 * r**(n-1)

# 극한식 검증
limit_expr = (4**n * an - 1) / (3 * 2**(n+1))
result = limit(limit_expr, n, oo)

if result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')