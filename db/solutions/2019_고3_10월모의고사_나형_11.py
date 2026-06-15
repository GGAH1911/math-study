import sympy as sp
a = sp.symbols('a', real=True)
mu, sigma = 5, 2
# P(X<=9-2a)=P(X>=3a-3) -> symmetric about mean: (9-2a)+(3a-3)=2*mu
sol = sp.solve(sp.Eq((9-2*a)+(3*a-3), 2*mu), a)
assert len(sol)==1
av = sol[0]
lo = 9-2*av
hi = 3*av-3
# CDF via erf
def P_leq(x):
    return sp.Rational(1,2)*(1+sp.erf((x-mu)/(sigma*sp.sqrt(2))))
# check the defining equation: P(X<=lo)==P(X>=hi)
lhs = P_leq(lo)
rhs = 1 - P_leq(hi)
assert sp.simplify(lhs-rhs)==0
# target probability P(lo<=X<=hi)
prob = sp.nsimplify(P_leq(hi)-P_leq(lo))
val = float(prob)
# compare with table-based value 2*0.4772=0.9544 (z=2)
expected = 0.9544
if abs(val-expected) < 5e-4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', val)
