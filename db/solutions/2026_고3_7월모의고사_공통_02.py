import sympy as sp
x, h = sp.symbols('x h')
f = x**2 + 3*x - 1
limit_value = sp.limit((f.subs(x, 3+h) - f.subs(x, 3)) / h, h, 0)
print('VERIFY_PASS' if limit_value == 9 else 'VERIFY_FAIL')