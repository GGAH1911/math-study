import sympy as sp
x = sp.Symbol('x')
f = 4*x**3 - 2*x
F = x**4 - x**2 + 4
print('VERIFY_PASS' if F.subs(x, 0) == 4 and F.subs(x, 2) == 16 else 'VERIFY_FAIL')