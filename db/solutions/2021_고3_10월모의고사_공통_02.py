import sympy as sp
x = sp.Symbol('x')
integrand = (x + 1)**2
result = sp.integrate(integrand, (x, 0, 3))
if result == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')