import sympy as sp

t = sp.Symbol('t', real=True)
s = sp.Symbol('s', real=True)
a = sp.Rational(1, 4)
f_expr = a * (t + 7) * (t - 6)

def g_val(xv):
    xv = sp.nsimplify(xv)
    fs = a * (s + 7) * (s - 6)
    if xv == 0:
        return sp.Integer(0)
    if xv > 0:
        int_abs = sp.integrate(sp.Abs(fs), (s, 0, xv))
    else:
        int_abs = -sp.integrate(sp.Abs(fs), (s, xv, 0))
    int_f = sp.integrate(fs, (s, 0, xv))
    return sp.simplify(int_abs + sp.Abs(int_f))

# (가): g(x)=0 on [-7, 0]
test_a = [sp.Integer(-7), sp.Rational(-9,2), sp.Integer(-2), sp.Integer(0)]
ok_a = all(g_val(x) == 0 for x in test_a)
# Below -7: should be < 0
ok_a = ok_a and g_val(sp.Integer(-8)) < 0

# (나): g(x)=81 on [4p, 7p] with p=3/2
p = sp.Rational(3, 2)
test_b = [4*p, sp.Integer(7), sp.Integer(8), 7*p]
ok_b = all(g_val(x) == 81 for x in test_b)
ok_b = ok_b and g_val(sp.Integer(5)) != 81 and g_val(sp.Integer(11)) != 81

# f(-10) = 12
ok_f = (f_expr.subs(t, -10) == 12)

# Leading coefficient positive
ok_lead = (a > 0)

print('VERIFY_PASS' if (ok_a and ok_b and ok_f and ok_lead) else 'VERIFY_FAIL')