import sympy as sp

CANDIDATE = 8

t = sp.Symbol('t')
x = t**3 - 5*t**2 + 6*t
v = sp.diff(x, t)
a = sp.diff(v, t)

a_at_3 = a.subs(t, 3)

if a_at_3 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')