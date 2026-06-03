from sympy import symbols, limit, Rational, oo, simplify
n = symbols('n', positive=True, integer=True)
# 원래 조건: 첫째항 1, 공차 2 등차수열
a1 = 1
d = 2
a_n = a1 + (n-1)*d  # = 2n - 1
expr = a_n / (3*n + 1)
L = limit(expr, n, oo)
ans = Rational(2, 3)
print('VERIFY_PASS' if simplify(L - ans) == 0 else 'VERIFY_FAIL')
