from sympy import symbols, diff, solve, Rational
x, a = symbols('x a', real=True)
f = x**3 + 3*a*x**2 + 4*a
fp = diff(f, x)
cands = []
for a_val in solve(a**3 + a + 10, a):
    if a_val.is_real and a_val != 0:
        cands.append(a_val)
ok = False
for a_val in cands:
    if a_val >= 0:
        continue
    crits = solve(fp.subs(a, a_val), x)
    vals = [f.subs({a: a_val, x: c}) for c in crits]
    mn = min(vals)
    if mn == -40:
        f2 = f.subs({a: a_val, x: 2})
        if f2 == -24:
            ok = True
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
