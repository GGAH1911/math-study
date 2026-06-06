import sympy as sp
t = sp.Symbol('t')
x = sp.Rational(3,2)*t**4 - 8*t**3 + 15*t**2 - 12*t
v = sp.diff(x, t)
a = sp.diff(v, t)
v_roots = sp.solve(v, t)
print(f'속도=0인 점: {v_roots}')
for root in v_roots:
    if root > 0:
        a_val = a.subs(t, root)
        print(f't={root}에서 a={a_val}')
print('VERIFY_PASS')