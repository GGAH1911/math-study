import sympy as sp
x = sp.Symbol('x')
f = 4*x**4 + 4*x**3
integrand = f / (1 + x)
integral = sp.integrate(integrand, (x, 0, 1))
result = float(integral)
if abs(result - 1.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')