from sympy import *

sqrt5 = sqrt(5)
a_val = Rational(3,1)/sqrt5
b_val = 2*a_val
r_val = sqrt(a_val**2 + b_val**2)

# 1) radius = 3
assert simplify(r_val - 3) == 0, 'radius fail'

# 2) B on C2 and on x-axis
C2_center = (-a_val, -b_val)
B = (-2*a_val, 0)
dist_B = sqrt((B[0]-C2_center[0])**2 + (B[1]-C2_center[1])**2)
assert simplify(dist_B - 3) == 0, 'B not on C2'
assert B[1] == 0, 'B not on x-axis'

# 3) tangent slope at B = a/b = 1/2
rad_vec = (B[0]-C2_center[0], B[1]-C2_center[1])  # (-a, b)
tangent_slope = rad_vec[1]/(-rad_vec[0]) # perpendicular slope = a/b... wait
# radius direction: (-a, b), perpendicular direction: (b, a), slope = a/b
slope = a_val/b_val
assert simplify(slope - Rational(1,2)) == 0, 'slope fail'

# 4) PQ = 6 for perpendicular pair (verify for specific theta)
theta = symbols('theta', real=True)
OP2 = 4*(a_val*cos(theta) + b_val*sin(theta))**2
OQ2 = 4*(a_val*sin(theta) - b_val*cos(theta))**2
PQ2 = simplify(OP2 + OQ2)
assert simplify(PQ2 - 36) == 0, 'PQ!=6 fail'

# 5) distance from A to tangent line l: x - 2y + 6/sqrt(5) = 0
A_pt = (a_val, b_val)
line_val = A_pt[0] - 2*A_pt[1] + 6/sqrt5
dist = Abs(line_val)/sqrt(5)
dist_s = simplify(dist)

if simplify(dist_s - Rational(3,5)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL:', dist_s)
