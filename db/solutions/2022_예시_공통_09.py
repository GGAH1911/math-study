from sympy import symbols, diff, solve, Rational
x, t = symbols('x t')
f = -x**3 - x**2 + x
fp = diff(f, x)
# tangent at x=t passes through origin: f(t) - t*f'(t) = 0
expr = f.subs(x, t) - t*fp.subs(x, t)
ts = solve(expr, t)
slopes = [fp.subs(x, tv) for tv in ts]
# Verify each tangent actually passes through origin and tangent to curve
ok = True
for tv in ts:
    m = fp.subs(x, tv)
    y0 = f.subs(x, tv)
    # line y = m*x; check (tv, y0) on it
    if (m*tv - y0) != 0:
        ok = False
total = sum(slopes)
if ok and total == Rational(9, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
