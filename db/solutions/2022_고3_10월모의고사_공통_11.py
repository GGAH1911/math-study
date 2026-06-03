import sympy as sp
a, b = -7, 28
x = sp.Symbol('x', real=True)
f_expr = a*x**2 + b*x - 24
roots_base = sp.solve(f_expr, x)
count = 0
for root in roots_base:
    if 1 < root < 4: count += 1
for root in roots_base:
    if 4 < root + 4 < 8: count += 1
for root in roots_base:
    if 8 < root + 8 < 10: count += 1
if count == 5:
    verified = all(sp.simplify(a*(r%4)**2 + b*(r%4) - 24) == 0 for r, _ in [(root, None) for root in roots_base])
    print('VERIFY_PASS' if verified else 'VERIFY_FAIL')
else:
    print('VERIFY_FAIL')