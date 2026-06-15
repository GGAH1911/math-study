import sympy as sp
theta = sp.Symbol('theta', real=True, positive=True)
r = 8
l = 6 * sp.pi
eq = sp.Eq(r * theta, l)
sol = sp.solve(eq, theta)
if sol and sol[0] == 3*sp.pi/4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')