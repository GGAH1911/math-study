import sympy as sp

a_val = sp.Rational(15, 32)
x, y, t = sp.symbols('x y t', positive=True, real=True)

# Parabola y = -a x^2 + 8 a x (a>0)
f = -a_val*x**2 + 8*a_val*x

# Vertex C and foot D
x_C = sp.Rational(4)
y_C = f.subs(x, x_C)
C = sp.Matrix([x_C, y_C])
D = sp.Matrix([x_C, 0])

# Find t (A=(4-t, y0), B=(4+t, y0)) such that triangle AOD area = 12
# y_A = -a(4-t)^2 + 8a(4-t)
T = sp.symbols('T', positive=True)
yA = f.subs(x, 4-T)
area_AOD = sp.Rational(1,2) * 4 * yA  # base OD=4 on x-axis, height = y_A
t_candidates = sp.solve(sp.Eq(area_AOD, 12), T)
# also need ratio condition t^2 = 16/5; pick t matching both
ratio_eqs = [tc for tc in t_candidates if sp.simplify(tc**2 - sp.Rational(16,5)) == 0]
assert ratio_eqs, f"No t satisfies both AOD area=12 and a=15/32. Candidates: {t_candidates}"
t_val = ratio_eqs[0]

A = sp.Matrix([4 - t_val, f.subs(x, 4 - t_val)])
B = sp.Matrix([4 + t_val, f.subs(x, 4 + t_val)])

# Verify A, B same y, both in 1st quadrant
assert sp.simplify(A[1] - B[1]) == 0
assert A[0] > 0 and A[1] > 0 and B[0] > 0 and B[1] > 0
assert A[0] < B[0]

# Line through D parallel to BC: slope m = (yC - yB)/(xC - xB)
m = sp.simplify((C[1] - B[1])/(C[0] - B[0]))
# y - 0 = m (x - 4) ; intersect with parabola
xE = sp.symbols('xE', real=True)
sol = sp.solve(sp.Eq(m*(xE - 4), f.subs(x, xE)), xE)
# Pick E in 4th quadrant: x>0, y<0
E = None
for s in sol:
    yE = m*(s - 4)
    if sp.simplify(s) > 0 and sp.simplify(yE) < 0:
        E = sp.Matrix([s, yE])
        break
assert E is not None, f"No E in 4th quadrant. sols={sol}"

def tri_area(P, Q, R):
    return sp.Rational(1,2) * sp.Abs((Q[0]-P[0])*(R[1]-P[1]) - (R[0]-P[0])*(Q[1]-P[1]))

area_CAB = sp.simplify(tri_area(C, A, B))
area_CEB = sp.simplify(tri_area(C, E, B))
area_AOD_check = sp.simplify(tri_area(sp.Matrix([0,0]), A, D))

ratio = sp.simplify(area_CAB / area_CEB)

ok_ratio = sp.simplify(ratio - sp.Rational(2,5)) == 0
ok_AOD   = sp.simplify(area_AOD_check - 12) == 0

print('VERIFY_PASS' if (ok_ratio and ok_AOD) else 'VERIFY_FAIL')
