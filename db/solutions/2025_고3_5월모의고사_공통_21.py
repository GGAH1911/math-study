import sympy as sp
x = sp.Symbol('x')
f = x * (x - 3)**2
result = f.subs(x, 8)
print('VERIFY_PASS' if result == 200 else 'VERIFY_FAIL')