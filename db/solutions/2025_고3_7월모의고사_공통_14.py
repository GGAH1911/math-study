from sympy import *
r = 3*sqrt(2)
AB = 12
AO = sqrt(AB**2 + r**2)
sin_a = r/AO
cos_a = sqrt(1 - sin_a**2)
A = Matrix([0, 0])
O = Matrix([AO, 0])
B = Matrix([AB*cos_a, AB*sin_a])
C = Matrix([AB*cos_a, -AB*sin_a])
assert simplify((B-O).dot(B-O) - r**2) == 0
assert simplify((C-O).dot(C-O) - r**2) == 0
t = symbols('t')
Px = B[0] + t*(-sin_a)
Py = B[1] + t*cos_a
eq1 = (Px-O[0])**2 + (Py-O[1])**2 - r**2
t_vals = solve(eq1, t)
t_P = [tv for tv in t_vals if simplify(tv) != 0][0]
P = Matrix([simplify(Px.subs(t,t_P)), simplify(Py.subs(t,t_P))])
assert simplify((P-O).dot(P-O) - r**2) == 0
assert simplify((P-B).dot(Matrix([cos_a,sin_a]))) == 0
s = symbols('s')
Qx = s*P[0]
Qy = s*P[1]
eq2 = (Qx-O[0])**2 + (Qy-O[1])**2 - r**2
s_vals = solve(eq2, s)
s_Q = [sv for sv in s_vals if simplify(sv-1) != 0][0]
Q = Matrix([simplify(Qx.subs(s,s_Q)), simplify(Qy.subs(s,s_Q))])
assert simplify((Q-O).dot(Q-O) - r**2) == 0
BQ = sqrt((B-Q).dot(B-Q))
QC = sqrt((Q-C).dot(Q-C))
assert simplify(BQ/QC - 3) == 0
area = Abs(B[0]*(Q[1]-C[1]) + Q[0]*(C[1]-B[1]) + C[0]*(B[1]-Q[1])) / 2
area = simplify(area)
expected = Rational(16,3)*sqrt(2)
if simplify(area - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {area}')