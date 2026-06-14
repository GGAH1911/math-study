import sympy as sp

x = sp.Symbol('x')
f = x**2 + x + 3
limit_value = sp.limit(f, x, 0)

if limit_value == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')