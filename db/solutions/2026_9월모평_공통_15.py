import sympy as sp
x, t = sp.symbols('x t', real=True)
f_expr = sp.Rational(1,4)*x**3 - sp.Rational(3,2)*x**2 + x

# (1) cubic, positive leading coef, f(0)=0
p = sp.Poly(f_expr, x)
assert p.degree()==3 and p.LC()>0 and f_expr.subs(x,0)==0

# (2) g'(x)=|f(x)|-|x|=0 has 4 distinct real roots: solve f^2 = x^2
roots = sorted(set(sp.solve(f_expr**2 - x**2, x)))
assert len(roots) == 4

# (3) sign change of g' at x=2 and x=6 -> extrema
def gp(v):
    return float(abs(f_expr.subs(x, v)) - abs(v))
for xi in [2, 6]:
    assert gp(xi - 0.001) * gp(xi + 0.001) < 0

# (4) f(6)*g(2) < 0 using numerical Simpson on original integrand |f(t)|-|t|
def integrand(tv):
    fv = float(f_expr.subs(x, tv))
    return abs(fv) - abs(tv)

def simpson(F, a, b, n=20000):
    if n % 2: n += 1
    h = (b-a)/n
    s = F(a) + F(b)
    for i in range(1, n):
        s += (4 if i%2==1 else 2) * F(a + i*h)
    return s*h/3

g2 = simpson(integrand, 0.0, 2.0)
f6 = float(f_expr.subs(x, 6))
assert f6 * g2 < 0

# (5) f(8) = 40
f8 = int(f_expr.subs(x, 8))
if f8 == 40:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
