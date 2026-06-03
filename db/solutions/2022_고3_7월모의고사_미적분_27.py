from fractions import Fraction
import numpy as np

A1 = np.array([0.0, 1.0])
B1 = np.array([0.0, 0.0])
C1 = np.array([2.0, 0.0])
D1 = np.array([2.0, 1.0])
E1 = (A1 + D1) / 2

# F1: intersection of B1D1 and C1E1
# B1D1: (2t,t); C1E1: (2-s,s) => t=s=2/3
F1 = np.array([4/3, 2/3])

# G1 on B1D1 with |G1E1|=|G1F1| => t=1/3
G1 = np.array([2/3, 1/3])

def tri_area(P, Q, R):
    return 0.5 * abs((Q[0]-P[0])*(R[1]-P[1]) - (R[0]-P[0])*(Q[1]-P[1]))

area1 = tri_area(C1, D1, F1)
area2 = tri_area(G1, F1, E1)
S1_frac = Fraction(1, 3) + Fraction(1, 6)  # = 1/2

# Verify G1E1 == G1F1
assert abs(np.linalg.norm(G1-E1) - np.linalg.norm(G1-F1)) < 1e-9

# Verify areas
assert abs(area1 - 1/3) < 1e-9
assert abs(area2 - 1/6) < 1e-9

# New rectangle: A2B2:B2C2=1:2 => t=2/5
t = Fraction(2, 5)
AB2 = t
BC2 = 2 - 3*t  # = 4/5
assert AB2 * 2 == BC2  # ratio 1:2

r = (AB2 / 1) ** 2  # area ratio = (2/5)^2 = 4/25
assert r == Fraction(4, 25)

limit = S1_frac / (1 - r)
if limit == Fraction(25, 42):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
