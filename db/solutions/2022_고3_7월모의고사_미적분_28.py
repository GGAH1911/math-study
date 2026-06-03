import sympy as sp
x = sp.Symbol('x', real=True)
# f(x) = 2 - (1/6) cos(2 pi x): even, period 1 (hence period 2), C^1
f = 2 - sp.Rational(1, 6) * sp.cos(2 * sp.pi * x)
# Check (가): even
c_even = sp.simplify(f.subs(x, -x) - f)
# Check (나): period 2
c_per = sp.simplify(f.subs(x, x + 2) - f)
# Check given integral 1: int_0^1 f dx = 2
g1 = sp.simplify(sp.integrate(f, (x, 0, 1)) - 2)
# Check given integral 2: int_{-1}^5 f(x)(x+cos 2 pi x) dx = 47/2
g2 = sp.simplify(sp.integrate(f * (x + sp.cos(2 * sp.pi * x)), (x, -1, 5)) - sp.Rational(47, 2))
# Compute target
df = sp.diff(f, x)
val = sp.simplify(sp.integrate(df * sp.sin(2 * sp.pi * x), (x, 0, 1)))
claimed = sp.pi / 6
if c_even == 0 and c_per == 0 and g1 == 0 and g2 == 0 and sp.simplify(val - claimed) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
