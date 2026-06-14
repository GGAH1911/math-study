import sympy as sp
x = sp.Symbol('x')
f = (x**2 + 9*x) / x
limit_value = sp.limit(f, x, 0)
if limit_value == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')