import sympy as sp
from sympy import sqrt, symbols, simplify

# Given: sin(theta) = sqrt(11)/6
sin_theta = sqrt(11)/6
cos_theta_sq = 1 - sin_theta**2
cos_theta = sqrt(cos_theta_sq)  # cos(theta) = 5/6

# Coordinates
D = (0, 3)
B = (3, 0)
C = (3, 3)

# G = C + 4*(-cos(theta), sin(theta))
G = (3 - 4*cos_theta, 3 + 4*sin_theta)
G_simplified = (simplify(G[0]), simplify(G[1]))

# E: CE perpendicular to CG, |CE| = 4
E = (3 + 4*sin_theta, 3 + 4*cos_theta)
E_simplified = (simplify(E[0]), simplify(E[1]))

# Distances
DG_vec = (G[0] - D[0], G[1] - D[1])
BE_vec = (E[0] - B[0], E[1] - B[1])

DG_dist_sq = simplify(DG_vec[0]**2 + DG_vec[1]**2)
BE_dist_sq = simplify(BE_vec[0]**2 + BE_vec[1]**2)

DG_dist = sqrt(DG_dist_sq)
BE_dist = sqrt(BE_dist_sq)

product = simplify(DG_dist * BE_dist)

if product == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')