import sympy as sp

p = sp.Integer(4)
x = sp.symbols('x', real=True)

def g_at(tv):
    tv = sp.sympify(tv)
    # |f(x)| = x + t solutions
    sols_outer = sp.solve(x**2 - p*x - x - tv, x)
    sols_inner = sp.solve(-x**2 + p*x - x - tv, x)
    valid = []
    eps = 1e-9
    for s in sols_outer:
        sn = float(sp.N(s))
        if sn <= eps or sn >= float(p) - eps:
            valid.append(s)
    for s in sols_inner:
        sn = float(sp.N(s))
        if -eps <= sn <= float(p) + eps:
            valid.append(s)
    if len(valid) < 2:
        return None
    vs = sorted(valid, key=lambda v: float(sp.N(v)))
    a, b = vs[0], vs[-1]
    integrand = sp.Piecewise(
        ((x**2 - p*x) - (x + tv), (x <= 0) | (x >= p)),
        ((-(x**2 - p*x)) - (x + tv), True)
    )
    return sp.simplify(sp.integrate(integrand, (x, a, b)))

g0 = g_at(0)
expected = sp.Rational(1, 2)
g_pos = g_at(sp.Rational(1, 10))
g_neg = g_at(sp.Rational(-1, 10))

cond1 = sp.simplify(g0 - expected) == 0
cond2 = float(sp.N(g_pos)) < float(sp.N(expected))
cond3 = float(sp.N(g_neg)) < float(sp.N(expected))

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
