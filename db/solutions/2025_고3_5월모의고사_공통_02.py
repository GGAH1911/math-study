import sympy as sp
h = sp.Symbol('h')
f = lambda x: x**3 - 2*x + 5
f1 = f(1)
f1_h = f(1 + h)
quotient = (f1_h - f1) / h
limit_val = sp.limit(quotient, h, 0)
if limit_val == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')