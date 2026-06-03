import sympy as sp
from sympy import summation, oo, limit

n = sp.Symbol('n', integer=True, positive=True)
N = sp.Symbol('N', integer=True, positive=True)

# a_n = 4 + (n-1)*3 = 1 + 3n
a_n = 1 + 3*n

# 일반항
term = a_n/n - (3*n + 7)/(n + 2)
term_simplified = sp.simplify(term)

# 망원급수 부분합 계산
partial_sum = summation(1/n - 1/(n+2), (n, 1, N))
partial_sum_simplified = sp.simplify(partial_sum)

# 극한 계산
S = limit(partial_sum_simplified, N, oo)

# 검증
if sp.simplify(term_simplified - (1/n - 1/(n+2))) == 0:
    if S == sp.Rational(3, 2):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')