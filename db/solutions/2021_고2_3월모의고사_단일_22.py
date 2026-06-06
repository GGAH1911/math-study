import sympy as sp
x = sp.Symbol('x')
P = x**3 + x**2 - 2*x
result = P.subs(x, 2)
if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')