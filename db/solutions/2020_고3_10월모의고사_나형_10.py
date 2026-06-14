import sympy as sp

CANDIDATE = sp.Rational(1, 6)

a = sp.Symbol('a', positive=True)
x = sp.Symbol('x')

area = sp.integrate(a*x - x**2, (x, 0, a))
area_coeff = sp.simplify(area / a**3)

if area_coeff == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')