import sympy as sp
x = sp.Symbol('x')
f = 2*x**3 + 3*x**2 - 12*x + 1
f_prime = sp.diff(f, x)
critical_points = sp.solve(f_prime, x)
values = sorted([float(f.subs(x, cp)) for cp in critical_points])
M = max(values)
m = min(values)
answer = M + m
if abs(answer - 15) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')