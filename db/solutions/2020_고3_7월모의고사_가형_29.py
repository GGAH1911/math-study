CANDIDATE = 120

import numpy as np

# Verify the limit S(theta)/r(theta) -> 8/3 as theta -> 0+
# and that 45a = CANDIDATE

def r_theta(t):
    return 2*np.sin(t) / (1 + np.sin(t))

def S_theta(t):
    c2 = np.cos(2*t)
    s2 = np.sin(2*t)
    return 8 * s2 * c2**2 / (1 + 2*c2)

# Numerical limit
thetas = [1e-3, 1e-4, 1e-5, 1e-6]
ratios = [S_theta(t)/r_theta(t) for t in thetas]
limit_numerical = ratios[-1]  # should be ~8/3

a = 8/3
result = 45 * a  # should be 120

# Check formulas at theta=pi/6
import sympy as sp
th = sp.pi/6
P = (2*sp.cos(2*th), 2*sp.sin(2*th))
Q_x = sp.Rational(2,1)/(1+2*sp.cos(2*th))
Q = (Q_x, sp.Integer(0))
R = (-2*sp.cos(4*th), -2*sp.sin(4*th))
B = (sp.Integer(2), sp.Integer(0))

# Check P,R on circle
assert sp.simplify(P[0]**2+P[1]**2 - 4) == 0, 'P not on circle'
assert sp.simplify(R[0]**2+R[1]**2 - 4) == 0, 'R not on circle'

# r(pi/6)
r_val = sp.Rational(2,1)*sp.sin(th)/(1+sp.sin(th))
print('r(pi/6)=', sp.simplify(r_val))

# Center
s_val = sp.Rational(2,1)/(1+sp.sin(th))
center = ((2-s_val)*sp.cos(2*th), (2-s_val)*sp.sin(2*th))
# Check distance from center to O equals r
dist_O = sp.sqrt(center[0]**2 + center[1]**2)
assert sp.simplify(dist_O - r_val) == 0, 'C does not pass through O'

# Check P,Q,R collinear
vec_PQ = (Q[0]-P[0], Q[1]-P[1])
vec_PR = (R[0]-P[0], R[1]-P[1])
cross = sp.simplify(vec_PQ[0]*vec_PR[1] - vec_PQ[1]*vec_PR[0])
assert cross == 0, 'P,Q,R not collinear'

# Check limit numerically
if abs(limit_numerical - 8/3) < 1e-4 and abs(result - CANDIDATE) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('limit=', limit_numerical, 'expected=', 8/3)
    print('45a=', result, 'CANDIDATE=', CANDIDATE)
