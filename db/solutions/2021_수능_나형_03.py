import sympy as sp
x = sp.Symbol('x')
f = (x**2 + 2*x - 8) / (x - 2)
limit_val = sp.limit(f, x, 2)
print('VERIFY_PASS' if limit_val == 6 else 'VERIFY_FAIL')