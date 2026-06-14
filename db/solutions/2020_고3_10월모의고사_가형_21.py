import numpy as np

CANDIDATE = 8.0/9.0  # limit value of S(theta)/theta as theta->0+

def angle_at(vertex, p1, p2):
    v1 = np.asarray(p1, float) - np.asarray(vertex, float)
    v2 = np.asarray(p2, float) - np.asarray(vertex, float)
    c = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    c = max(-1.0, min(1.0, c))
    return np.arccos(c)

def S_over_theta(theta):
    # original conditions, reconstructed from scratch
    A = np.array([0.0, 0.0])
    center = np.array([1.0, 0.0]); R = 1.0   # semicircle, diameter AB length 2
    # P = second intersection of ray from A at angle theta with the circle
    d = np.array([np.cos(theta), np.sin(theta)])
    ac = A - center
    b = 2.0*np.dot(d, ac)          # |d|=1 -> t^2 + b t = 0, t=0 is A
    P = A + (-b)*d
    # C=(xc,0) on AB with angle APC = 2 theta  (monotone in xc -> bisection)
    lo, hi = 1e-12, 1.999999
    for _ in range(120):
        mid = 0.5*(lo+hi)
        if angle_at(P, A, [mid,0.0]) - 2.0*theta > 0:
            hi = mid
        else:
            lo = mid
    C = np.array([0.5*(lo+hi), 0.0])
    # line through C perpendicular to CP ; D = foot of perpendicular from A (gives angle ADC=90)
    cp = P - C
    perp = np.array([-cp[1], cp[0]]); perp = perp/np.linalg.norm(perp)
    D = C + np.dot(A - C, perp)*perp
    # E = intersection of line AP and line CD
    M = np.array([[d[0], -perp[0]],[d[1], -perp[1]]])
    uv = np.linalg.solve(M, C - A)
    E = A + uv[0]*d
    # confirm the two given right-angle conditions hold for the reconstruction
    assert abs(angle_at(D, A, C) - np.pi/2) < 1e-7   # angle ADC = pi/2
    assert abs(angle_at(C, P, D) - np.pi/2) < 1e-7   # angle PCD = pi/2
    # area of triangle DEP
    area = 0.5*abs((E[0]-D[0])*(P[1]-D[1]) - (P[0]-D[0])*(E[1]-D[1]))
    return area/theta

est = S_over_theta(1e-4)
print('estimate of limit:', est)
if abs(est - CANDIDATE) < 1e-3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
