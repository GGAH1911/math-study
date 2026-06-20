import sympy as sp
x = sp.Symbol('x')
f = x**3 - 2*x**2
roots = sp.solve(f, x)
print('Roots:', roots)
integral = sp.integrate(f, (x, 0, 2))
area = sp.Abs(integral)
print('Integral value:', integral)
print('Area:', area)
if area == sp.Rational(4, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')