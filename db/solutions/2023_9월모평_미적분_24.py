import sympy as sp
x = sp.Symbol('x')
integrand = x * sp.cos(sp.pi/2 - x)
result = sp.integrate(integrand, (x, 0, sp.pi))
if sp.simplify(result - sp.pi) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')