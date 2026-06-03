import sympy as sp
x = sp.Symbol('x', positive=True, real=True)
expr = (sp.ln(2*x**2 + 3*x) - sp.ln(3*x)) / x
limit_val = sp.limit(expr, x, 0, '+')
if limit_val == sp.Rational(2, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')