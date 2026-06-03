import sympy as sp

t = sp.Symbol('t', positive=True)
x = sp.exp(2*t - 2)
y = sp.ln(t) / t

dxdt = sp.diff(x, t)
dydt = sp.diff(y, t)
dydx = sp.simplify(dydt / dxdt)

val = sp.simplify(dydx.subs(t, 1))
expected = sp.Rational(1, 2)

if sp.simplify(val - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
