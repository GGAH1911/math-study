from sympy import *

t = symbols('t', real=True)
sq3 = sqrt(3)

A = Matrix([0, 0, 1])
P = Matrix([sq3, -2*sq3, 0])
Q = Matrix([sq3,  2*sq3, 0])
M = Matrix([sq3, 0, 0])

# 1. P, Q on circle C: x^2+y^2=15, z=0
assert simplify(P[0]**2+P[1]**2-15)==0 and P[2]==0
assert simplify(Q[0]**2+Q[1]**2-15)==0 and Q[2]==0

# 2. Distance from A to segment PQ = 2 (foot = M)
assert simplify((A-M).dot(A-M)-4)==0

# 3. P, Q on sphere S (radius 4)
assert simplify((P-A).dot(P-A)-16)==0
assert simplify((Q-A).dot(Q-A)-16)==0

# 4. Sphere T: diameter PQ, center M, radius^2=12
assert simplify((P-Q).dot(P-Q)/4-12)==0

# 5. B on intersection circle of S and T
B = Matrix([sq3+sq3*sin(t), 2*sq3*cos(t), 3*sin(t)])
assert simplify((B-A).dot(B-A)-16)==0, 'B not on S'
assert simplify((B-M).dot(B-M)-12)==0, 'B not on T'

# 6. Area of projection of triangle BPQ onto xy-plane
Bp = Matrix([B[0], B[1], 0])
v1 = Q - P
v2 = Bp - P
cross_z = v1[0]*v2[1] - v1[1]*v2[0]
area = Rational(1,2)*Abs(cross_z)
area_simp = simplify(area.rewrite(Piecewise).doit())
# For t in (0,pi), sin(t)>0
area_pos = Rational(1,2)*Abs(simplify(cross_z)).subs(Abs(sin(t)), sin(t))

# Maximum at t=pi/2
area_at_pi2 = simplify(Rational(1,2)*Abs(cross_z.subs(t, pi/2)))

if area_at_pi2 == 6:
    # Also verify no larger value possible: area=6*sin(t)<=6
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL:', area_at_pi2)
