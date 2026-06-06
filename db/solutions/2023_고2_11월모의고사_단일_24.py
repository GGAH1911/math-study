import sympy as sp
x = sp.Symbol('x')
f = x**3 + 2*x**2 + 2
f_prime = sp.diff(f, x)
integral_expr = sp.integrate(f_prime, (x, 1, x))
integral_result = x**3 + 2*x**2 - 3
limit_expr = integral_result / (x - 1)
limit_value = sp.limit(limit_expr, x, 1)
print('VERIFY_PASS' if limit_value == 7 else 'VERIFY_FAIL')