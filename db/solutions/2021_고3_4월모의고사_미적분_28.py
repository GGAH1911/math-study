import sympy as sp

A1 = sp.Matrix([0,4]); B1 = sp.Matrix([0,0]); C1 = sp.Matrix([3,4])
t = sp.symbols('t', positive=True)
P = B1 + t*(C1-B1)
sols = sp.solve(P[0]**2 + (P[1]-2)**2 - 4, t)
t_v = max(sols)
D1 = B1 + t_v*(C1-B1)

semi = sp.pi*2**2/2
tri = sp.Rational(1,2)*abs(A1[0]*(B1[1]-D1[1]) + B1[0]*(D1[1]-A1[1]) + D1[0]*(A1[1]-B1[1]))
S1 = semi + tri

p,q,r = sp.symbols('p q r', positive=True)
sols2 = sp.solve([sp.Eq(r,4-q), sp.Eq(r,(3*q-4*p)/5), sp.Eq(sp.sqrt(p**2+(q-2)**2), 2+r)], [p,q,r], dict=True)
sol = min(sols2, key=lambda s: s[r])
p_v, q_v, r_v = sol[p], sol[q], sol[r]

assert sp.simplify(sp.sqrt(p_v**2 + (q_v-2)**2) - (2+r_v)) == 0
assert sp.simplify((4 - q_v) - r_v) == 0
assert sp.simplify((3*q_v - 4*p_v)/5 - r_v) == 0

diameter_O2 = 2*r_v
ratio_sq = (diameter_O2/4)**2
S_inf = sp.simplify(S1/(1-ratio_sq))

expected = sp.Rational(32,15)*sp.pi + sp.Rational(512,125)
if sp.simplify(S_inf - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', S_inf, expected)
