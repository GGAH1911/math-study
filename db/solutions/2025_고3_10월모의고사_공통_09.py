import sympy as sp
t = sp.Symbol('t')
x1 = -t**3 + 7*t**2 - 10*t
x2 = t**2 + 2*t
v1 = sp.diff(x1, t)
v2 = sp.diff(x2, t)
eq = sp.Eq(v1, v2)
t_solutions = sp.solve(eq, t)
print(f't solutions: {t_solutions}')
for t_val in t_solutions:
    if t_val >= 0:
        pos1 = x1.subs(t, t_val)
        pos2 = x2.subs(t, t_val)
        distance = abs(pos2 - pos1)
        print(f'At t={t_val}: x1={pos1}, x2={pos2}, distance={distance}')
        if distance == 8:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')