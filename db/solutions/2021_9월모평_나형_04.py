import sympy as sp
x = sp.Symbol('x')
f = (x**2 + 9*x + 8) / (x + 1)
limit_val = sp.limit(f, x, -1)
if limit_val == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')