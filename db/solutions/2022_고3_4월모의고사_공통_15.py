import numpy as np
from fractions import Fraction

# Concrete realisation satisfying the problem statement:
# Circle radius R = 5*sqrt(2) (within 5 < R < 5*sqrt(5))
R = 5*np.sqrt(2)
A = np.array([0.0, 5*np.sqrt(2)])
B = np.array([-4*np.sqrt(2), 3*np.sqrt(2)])
C = np.array([-5*np.sqrt(2), 0.0])
D = np.array([4*np.sqrt(2), 3*np.sqrt(2)])

# 1) all four points lie on the circle of radius R about the origin
for P in (A,B,C,D):
    assert abs(np.linalg.norm(P)-R) < 1e-9
assert 5 < R < 5*np.sqrt(5)

# 2) |AB| = |AD| = k
AB = np.linalg.norm(A-B); AD = np.linalg.norm(A-D)
assert abs(AB-AD) < 1e-9
k = AB

# 3) |AC| = 10
AC = np.linalg.norm(A-C)
assert abs(AC-10) < 1e-9

# 4) Area(ABCD) = 40 (shoelace, vertices in cyclic order on circle)
def shoelace(pts):
    s = 0.0
    n = len(pts)
    for i in range(n):
        x1,y1 = pts[i]; x2,y2 = pts[(i+1)%n]
        s += x1*y2 - x2*y1
    return abs(s)/2
area = shoelace([A,B,C,D])
assert abs(area-40) < 1e-9

# 5) Recover (가)=f(k)=100-k^2 via cos(ACB) on triangle ABC
BC = np.linalg.norm(B-C)
cos_ACB_direct = (BC**2 + AC**2 - AB**2)/(2*BC*AC)
cos_ACB_form   = (1/20)*(BC + (100 - k**2)/BC)
assert abs(cos_ACB_direct - cos_ACB_form) < 1e-9

# 6) Recover sin(BAD)=4/5  -> (나)=p=4/5
BA = B-A; DA = D-A
cos_BAD = np.dot(BA,DA)/(np.linalg.norm(BA)*np.linalg.norm(DA))
sin_BAD = np.sqrt(1-cos_BAD**2)
assert abs(sin_BAD - 4/5) < 1e-9

# 7) Recover BD:R = 8:5  -> (다)=q=8/5
BD = np.linalg.norm(B-D)
assert abs(BD/R - 8/5) < 1e-9

# 8) Compute f(10p)/q with f(k)=100-k^2, p=4/5, q=8/5
p = Fraction(4,5); q = Fraction(8,5)
def f(x): return 100 - x*x
val = f(10*p)/q
print('VERIFY_PASS' if val == Fraction(45,2) else 'VERIFY_FAIL')
