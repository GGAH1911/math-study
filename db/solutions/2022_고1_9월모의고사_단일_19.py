from sympy import sqrt, Rational, simplify, Symbol, solve, Eq

# Original problem data
A = (Rational(-1), Rational(4))
B = (Rational(-3), Rational(0))
C = (Rational(0), Rational(-2))
D = (Rational(1), Rational(3))

# Compute (가) f(x): line through A, perpendicular to BD, from scratch using original points
slope_BD = (D[1]-B[1])/(D[0]-B[0])
slope_l1 = -1/slope_BD
# l1: y = slope_l1*(x - A[0]) + A[1]
def f(x):
    return slope_l1*(x - A[0]) + A[1]
# verify A on l1
assert simplify(f(A[0]) - A[1]) == 0

# Find E: intersection of circle (center A, radius |BD|) with l1, closer to C
BD_len = sqrt((D[0]-B[0])**2 + (D[1]-B[1])**2)
x = Symbol('x', real=True)
sols = solve(Eq((x-A[0])**2 + (f(x)-A[1])**2, BD_len**2), x)
candidates = [(s, f(s)) for s in sols]
E = min(candidates, key=lambda p: (p[0]-C[0])**2 + (p[1]-C[1])**2)

# (나) g(x): line through C and E
slope_l2 = (E[1]-C[1])/(E[0]-C[0])
def g(x):
    return slope_l2*(x - C[0]) + C[1]
assert simplify(g(C[0]) - C[1]) == 0
assert simplify(g(E[0]) - E[1]) == 0

# (다) alpha: side length of square PQRS with A on PQ, B on QR, C on RS, D on SP
# PQ parallel to l_2 through A; QR perpendicular through B; RS = l_2; SP perpendicular through D
# All lines:
# PQ: y = slope_l2*(x - A[0]) + A[1]
# QR: y = (-1/slope_l2)*(x - B[0]) + B[1]
# RS: y = slope_l2*(x - C[0]) + C[1]
# SP: y = (-1/slope_l2)*(x - D[0]) + D[1]
m = slope_l2
mp = -1/m

def intersect(line1, line2):
    # each line: (slope, point)
    s1, p1 = line1
    s2, p2 = line2
    xs = Symbol('xs', real=True)
    sol = solve(Eq(s1*(xs - p1[0]) + p1[1], s2*(xs - p2[0]) + p2[1]), xs)[0]
    ys = s1*(sol - p1[0]) + p1[1]
    return (simplify(sol), simplify(ys))

P = intersect((m, A), (mp, D))   # PQ ∩ SP
Q = intersect((m, A), (mp, B))   # PQ ∩ QR
R = intersect((m, C), (mp, B))   # RS ∩ QR
S = intersect((m, C), (mp, D))   # RS ∩ SP

# Side lengths
def dist(p1, p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

L_PQ = simplify(dist(P, Q))
L_QR = simplify(dist(Q, R))
L_RS = simplify(dist(R, S))
L_SP = simplify(dist(S, P))
assert simplify(L_PQ - L_QR) == 0
assert simplify(L_QR - L_RS) == 0
assert simplify(L_RS - L_SP) == 0

# Verify A on segment PQ, B on QR, C on RS, D on SP
def on_seg(pt, s1, s2):
    if s2[0] != s1[0]:
        t = (pt[0]-s1[0])/(s2[0]-s1[0])
    else:
        t = (pt[1]-s1[1])/(s2[1]-s1[1])
    t = simplify(t)
    cx = simplify(s1[0] + t*(s2[0]-s1[0]) - pt[0])
    cy = simplify(s1[1] + t*(s2[1]-s1[1]) - pt[1])
    return cx == 0 and cy == 0 and 0 <= t <= 1

assert on_seg(A, P, Q)
assert on_seg(B, Q, R)
assert on_seg(C, R, S)
assert on_seg(D, S, P)

alpha = L_PQ

result = simplify(Rational(3,4)*f(alpha) - g(alpha))
expected = 4 - 7*sqrt(2)
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)
