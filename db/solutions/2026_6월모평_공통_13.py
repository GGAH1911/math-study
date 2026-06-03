import sympy as sp
x = sp.symbols('x', real=True)
f = 3*x**2 - 7*x + 2
g = sp.Rational(1,3)*x - sp.Rational(2,3)
roots = sorted(sp.solve(f - g, x))
alpha, beta = roots[0], roots[1]
assert alpha == sp.Rational(4,9) and beta == 2
k_val = sp.Rational(8, 3)
A = sp.integrate(f - g, (x, 0, alpha))
B = sp.integrate(g - f, (x, alpha, beta))
C = sp.integrate(f - g, (x, beta, k_val))
if sp.simplify(A + C - B) == 0 and k_val > 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
