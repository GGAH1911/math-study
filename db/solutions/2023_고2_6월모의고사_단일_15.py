import numpy as np
from sympy import *

a_val = Rational(2,3) * sqrt(3) * pi

A = (0, 2*a_val)
B = (-pi, a_val/2)
C = (pi, a_val/2)

dist_AB = sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)
dist_AC = sqrt((A[0]-C[0])**2 + (A[1]-C[1])**2)
dist_BC = sqrt((B[0]-C[0])**2 + (B[1]-C[1])**2)

dist_AB_simp = simplify(dist_AB)
dist_AC_simp = simplify(dist_AC)
dist_BC_simp = simplify(dist_BC)

if dist_AB_simp == dist_AC_simp == dist_BC_simp:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')