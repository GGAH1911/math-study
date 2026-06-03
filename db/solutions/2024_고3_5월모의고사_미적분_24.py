import sympy as sp
from sympy import limit, oo, Sum, symbols

d = 3
n, N = symbols('n N', integer=True, positive=True)

# 등차수열 a_n = 1 + (n-1)*d
def a_n(k, d_val):
    return 1 + (k - 1) * d_val

# 망원급수 부분합: S_N = 1/a_1 - (N+1)/a_{N+1}
S_N = 1 / a_n(1, d) - (N + 1) / a_n(N + 1, d)

# N -> 무한대에서의 극한
result = limit(S_N, N, oo)

# 검증
if result == sp.Rational(2, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')