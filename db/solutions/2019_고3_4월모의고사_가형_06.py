import sympy as sp
x = sp.Symbol('x', positive=True)
integrand = 1 / (x * sp.sqrt(x))
result = sp.integrate(integrand, (x, 1, 16))
expected = sp.Rational(3, 2)
if result == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}, expected {expected}')