import sympy as sp
h = sp.Symbol('h')
f = lambda x: x**2 - 2*x + 3
f3 = f(3)
f3_plus_h = f(3 + h)
limit_result = sp.limit((f3_plus_h - f3) / h, h, 0)
if limit_result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')