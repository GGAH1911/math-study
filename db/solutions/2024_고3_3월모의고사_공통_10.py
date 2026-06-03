import sympy as sp
t = sp.Symbol('t')
v1 = 3*t**2 - 6*t - 2
v2 = -2*t + 6
xP = sp.integrate(v1, (t, 0, t))
xQ = sp.integrate(v2, (t, 0, t))
# Find meeting times
meeting_eq = sp.expand(xP - xQ)
roots = sp.solve(meeting_eq, t)
positive_roots = [r for r in roots if r > 0]
T = max(positive_roots)
assert T == 4, f'Meeting time should be 4, got {T}'
# Verify positions match at t=4
assert xP.subs(t, 4) == xQ.subs(t, 4) == 8, 'Positions do not match at t=4'
# Compute distance Q travels
dist = sp.integrate(sp.Abs(v2), (t, 0, T))
assert dist == 10, f'Distance should be 10, got {dist}'
print('VERIFY_PASS')
