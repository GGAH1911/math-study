import sympy as sp
t = sp.symbols('t', real=True, positive=True)
P = sp.Matrix([t, 2*t**2 + 1])
Q = sp.Matrix([t, -(t-3)**2 + 1])
A = sp.Matrix([0, 1])
B = sp.Matrix([3, 1])

def shoelace(pts):
    s = 0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i+1) % n]
        s += x1*y2 - x2*y1
    return sp.Abs(s) / 2

area = shoelace([(P[0], P[1]), (A[0], A[1]), (Q[0], Q[1]), (B[0], B[1])])
area_simplified = sp.simplify(area)
# minimize over 0 < t < 3
crit = sp.solve(sp.diff(area_simplified, t), t)
vals = [area_simplified.subs(t, c) for c in crit if c.is_real and 0 < c < 3]
min_area = sp.simplify(min(vals))
print('VERIFY_PASS' if min_area == 9 else 'VERIFY_FAIL')
