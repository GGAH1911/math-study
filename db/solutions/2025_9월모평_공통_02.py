import sympy as sp
h = sp.Symbol('h')
f = lambda x: x**3 + 3*x**2 - 5
f1 = f(1)
f1h = f(1 + h)
diff_quotient = (f1h - f1) / h
limit_result = sp.limit(diff_quotient, h, 0)
if limit_result == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')