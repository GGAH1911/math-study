import sympy as sp
h = sp.Symbol('h')
f = lambda x: 2*x**2 + x + 2
diff_quotient = (f(1+h) - f(1))/h
limit_result = sp.limit(diff_quotient, h, 0)
if limit_result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')