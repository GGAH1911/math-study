import sympy as sp
h = sp.Symbol('h')
f = lambda x: x**2 - x + 1
f_at_1 = f(1)
f_at_1_plus_h = f(1 + h)
expression = (f_at_1_plus_h - f_at_1) / h
limit_result = sp.limit(expression, h, 0)
if limit_result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')