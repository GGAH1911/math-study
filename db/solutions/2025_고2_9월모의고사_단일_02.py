import sympy as sp
x = sp.Symbol('x')
f = (3*x + 2) / ((x+1)**2 - x**2)
limit_val = sp.limit(f, x, sp.oo)
if sp.simplify(limit_val - sp.Rational(3, 2)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')