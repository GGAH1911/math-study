import sympy as sp
x = sp.Symbol('x')
a, b = -2, -8
f = x**2 + a*x + b
ineq = f <= 0
sol = sp.solve_univariate_inequality(ineq, x, relational=False)
if sol == sp.Interval(-2, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')