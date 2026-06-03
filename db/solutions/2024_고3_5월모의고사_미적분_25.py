import sympy as sp
from fractions import Fraction

t = sp.symbols('t', positive=True)
q = sp.symbols('q', real=True)
# 원래 조건: P=(t, e^{2t}-1), Q=(q,0), PQ=OQ
P = sp.Matrix([t, sp.exp(2*t)-1])
Q = sp.Matrix([q, 0])
O = sp.Matrix([0, 0])
PQ2 = (P-Q).dot(P-Q)
OQ2 = (Q-O).dot(Q-O)
sol = sp.solve(sp.Eq(PQ2, OQ2), q)
# 유일한 q(t)
f = [s for s in sol]
assert len(f) == 1, f
ft = sp.simplify(f[0])
lim = sp.limit(ft/t, t, 0, '+')
ans = sp.Rational(5,2)
print('VERIFY_PASS' if sp.simplify(lim - ans) == 0 else 'VERIFY_FAIL')
