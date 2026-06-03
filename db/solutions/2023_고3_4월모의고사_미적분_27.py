import numpy as np
from numpy import sin, cos, pi

def P(theta):
    return np.array([sin(2*theta), 1 - cos(2*theta)])

def Q(theta):
    return np.array([sin(2*theta/3), 1 - cos(2*theta/3)])

def f(theta):
    op = P(theta)
    oq = Q(theta)
    cross = op[0]*oq[1] - op[1]*oq[0]
    return 0.5 * abs(cross)

# Verify limit = 4/9
thetas = np.array([1e-3, 1e-4, 1e-5, 1e-6])
ratios = f(thetas) / thetas**3
target = 4/9

# Check angle condition angle OPQ = theta/3 for a sample theta
theta_test = 0.5
Pv = P(theta_test)
Qv = Q(theta_test)
PO = np.array([0,0]) - Pv
PQ = Qv - Pv
cos_angle = np.dot(PO, PQ) / (np.linalg.norm(PO) * np.linalg.norm(PQ))
angle_opq = np.arccos(np.clip(cos_angle, -1, 1))
angle_expected = theta_test / 3

limit_ok = np.allclose(ratios, target, rtol=1e-3)
angle_ok = abs(angle_opq - angle_expected) < 1e-8

if limit_ok and angle_ok:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: limit_ok={limit_ok}, ratios={ratios}, angle_ok={angle_ok}, angle_opq={angle_opq}, expected={angle_expected}')
