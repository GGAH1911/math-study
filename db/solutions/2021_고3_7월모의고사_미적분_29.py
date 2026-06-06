import sympy as sp
a, b, x = 1, 1, sp.Symbol('x')
g = a*x**3 + x**2 + b*x + 1
result = g.subs(x, 2)
if result == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')