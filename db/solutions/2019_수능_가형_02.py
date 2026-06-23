import sympy as sp
x = sp.Symbol('x')
expr = (x**2 + 5*x) / sp.ln(1 + 3*x)
limit_val = sp.limit(expr, x, 0)
if limit_val == sp.Rational(5, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')