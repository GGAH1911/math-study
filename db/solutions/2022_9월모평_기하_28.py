import numpy as np
from sympy import *

x, y, t = symbols('x y t', real=True)

# 타원
a2, b2 = 16, 12
c = sqrt(a2 - b2)  # =2
F = Matrix([c, 0])
Fp = Matrix([-c, 0])  # F'

# 접선 l at P(2,3): x+2y=8
# P on ellipse check
P = Matrix([2, 3])
assert simplify(P[0]**2/16 + P[1]**2/12 - 1) == 0, 'P not on ellipse'

# S: l meets x-axis
S = Matrix([8, 0])
assert S[0] + 2*S[1] == 8

# Line through F parallel to l: x+2y=2
# Intersection with ellipse
y_Q_pos = Rational(3,4)*(1 + sqrt(5))
x_Q = 2 - 2*y_Q_pos
Q = Matrix([x_Q, y_Q_pos])
assert simplify(Q[0]**2/16 + Q[1]**2/12 - 1) == 0, 'Q not on ellipse'
assert Q[0] < 0 and Q[1] > 0, 'Q not in 2nd quadrant'

# R: intersection of F'Q and l
# Parametric: Fp + t*(Q - Fp), find t such that x+2y=8
direction = Q - Fp
t_val = solve((Fp[0] + t*direction[0]) + 2*(Fp[1] + t*direction[1]) - 8, t)[0]
R = Fp + t_val * direction
assert simplify(R[0] + 2*R[1] - 8) == 0, 'R not on l'

# Perimeter
SR = sqrt((R[0]-S[0])**2 + (R[1]-S[1])**2)
RFp = sqrt((R[0]-Fp[0])**2 + (R[1]-Fp[1])**2)
SFp = sqrt((S[0]-Fp[0])**2 + (S[1]-Fp[1])**2)

perimeter = simplify(SR + RFp + SFp)
print('Perimeter =', perimeter)
if simplify(perimeter - 30) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', float(perimeter))
