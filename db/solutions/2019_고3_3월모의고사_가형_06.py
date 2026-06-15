import sympy as sp
x = sp.Symbol('x')
f = 2*x*sp.sqrt(x**2 + 1)
result = sp.integrate(f, (x, 0, sp.sqrt(3)))
expected = sp.Rational(14, 3)
if sp.simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')