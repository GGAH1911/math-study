import sympy as sp

CANDIDATE = 48

t, u = sp.symbols('t u', real=True)
# derived parameters from the problem conditions
a = -3
b = 3*sp.E

# h(t) = e^{a t} + b t  (g = h(f), f = sin(pi x/2))
h = sp.exp(a*t) + b*t
hp = sp.diff(h, t)

# (나)+critical: minimum at t0 with h(t0)=0, and t0 = 1/a
t0 = [s for s in sp.solve(hp, t) if s.is_real][0]
assert sp.simplify(t0 - sp.Rational(1,1)/a) == 0, 't0 != 1/a'
assert sp.simplify(t0 - sp.Rational(-1,3)) == 0, 't0 mismatch'
assert sp.simplify(h.subs(t, t0)) == 0, 'h(t0)!=0 violates (나)'
assert -1 < t0 < 0, 't0 not in (-1,0): (가) would fail'

# two distinct local maxima at f=1, f=-1, sum = e^3 + e^-3
M1, M2 = h.subs(t, 1), h.subs(t, -1)
assert sp.simplify(M1 + M2 - (sp.exp(3) + sp.exp(-3))) == 0, 'max-sum mismatch'
assert sp.simplify(M1 - M2) != 0, 'maxima not distinct'

# m = #extrema on (0,12): 6 critical pts (odd ints) + 6 crossings f=t0
m = 12

# integral: alpha_3=3 (u=-1) -> alpha_4 in (3,5) (u=t0); cos(pi x/2)dx=(2/pi)du
integrand = (sp.exp(a*u) + b*u) * (sp.Integer(2)/sp.pi)
I = sp.integrate(integrand, (u, -1, t0))
val = sp.simplify(m*sp.pi*I)   # = p e^3 + q e

Es = sp.symbols('Es', positive=True)
val2 = sp.expand(val.subs(sp.exp(3), Es**3).subs(sp.E, Es))
poly = sp.Poly(val2, Es)
p = poly.coeff_monomial(Es**3)
q = poly.coeff_monomial(Es)
assert sp.simplify(val - (p*sp.exp(3) + q*sp.E)) == 0, 'p,q extraction failed'
assert int(p) == p and int(q) == q, 'p,q not integers'

result = int(p - q)
print('VERIFY_PASS' if result == CANDIDATE else 'VERIFY_FAIL')
