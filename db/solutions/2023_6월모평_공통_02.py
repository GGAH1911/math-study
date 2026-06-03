import sympy as sp
h = sp.Symbol('h')
f = lambda x: x**3 + 9
result = sp.limit((f(2+h) - f(2))/h, h, 0)
if result == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')