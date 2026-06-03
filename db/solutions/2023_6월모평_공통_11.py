import sympy as sp
t, s = sp.symbols('t s', real=True)
v1 = 2 - t
v2 = 3*t
xP = sp.integrate(v1.subs(t, s), (s, 0, t))
roots = [r for r in sp.solve(sp.Eq(xP, 0), t) if r != 0 and r > 0]
T = roots[0]
distQ = sp.integrate(sp.Abs(v2.subs(t, s)), (s, 0, T))
print('VERIFY_PASS' if sp.simplify(distQ - 24) == 0 else 'VERIFY_FAIL')
