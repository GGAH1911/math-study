import sympy as sp
x = sp.Symbol('x')
a, b = -8, 10
equation = 2*x**2 + a*x + b
roots = sp.solve(equation, x)
if 2 - sp.I in roots and 2 + sp.I in roots:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')