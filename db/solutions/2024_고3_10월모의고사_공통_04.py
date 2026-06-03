import sympy as sp
x = sp.Symbol('x')
integral1 = sp.integrate(3*x + 4, (x, 1, 2))
integral2 = sp.integrate(3*x**2 - 3*x, (x, 1, 2))
total = integral1 + integral2
print('VERIFY_PASS' if total == 11 else f'VERIFY_FAIL: {total}')