import sympy as sp
x = sp.Symbol('x')
f = x**3 - sp.Rational(3,2)*x**2 - 6*x + sp.Rational(1,2)
f_prime = sp.diff(f, x)
crit_points = sp.solve(f_prime, x)
max_val = max([f.subs(x, pt) for pt in crit_points if f_prime.subs(x, pt-0.001)*f_prime.subs(x, pt+0.001) < 0])
print('VERIFY_PASS' if max_val == 4 else 'VERIFY_FAIL')