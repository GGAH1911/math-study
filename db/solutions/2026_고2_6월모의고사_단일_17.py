import numpy as np
from sympy import *

cos_alpha = Rational(1,1)/sqrt(5)
sin_alpha = Rational(2,1)/sqrt(5)
cos_beta = Rational(-2,1)/sqrt(5)
sin_beta = Rational(1,1)/sqrt(5)

# Points
A = (2*cos_alpha, 2*sin_alpha)
B = (2*cos_beta, 2*sin_beta)

# Verify conditions
AB_dist_sq = (A[0]-B[0])**2 + (A[1]-B[1])**2
assert simplify(AB_dist_sq - 8) == 0, f'AB distance check failed'
assert simplify(cos_alpha * sin_beta - Rational(1,5)) == 0, f'cos*sin check failed'

# Feet of perpendiculars
C = (A[0], 0)
D = (B[0], 0)

# Shoelace formula
vertices = [A, B, D, C]
area = 0
for i in range(len(vertices)):
    j = (i+1) % len(vertices)
    area += vertices[i][0]*vertices[j][1] - vertices[j][0]*vertices[i][1]
area = abs(area)/2

if simplify(area - Rational(18,5)) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {area}')