import sympy as sp
x = sp.Symbol('x')
f = (sp.exp(4*x) - 1) / (3*x)
limit_result = sp.limit(f, x, 0)
expected = sp.Rational(4, 3)
if limit_result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')