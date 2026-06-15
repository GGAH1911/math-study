import sympy as sp
n = sp.Symbol('n', integer=True, positive=True)
a_val = 15
f = (a_val + sp.Rational(1,4)**n) / (5 + sp.Rational(1,2)**n)
limit_result = sp.limit(f, n, sp.oo)
if limit_result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')