import numpy as np

def compute_ratio(theta):
    A = np.array([-1.0, 0.0])
    B = np.array([1.0, 0.0])
    O = np.array([0.0, 0.0])
    P = np.array([np.cos(2*theta), np.sin(2*theta)])
    Q = np.array([np.cos(4*theta), -np.sin(4*theta)])
    R = -Q
    D = 4*np.cos(2*theta)**2 + 2*np.cos(2*theta) - 1
    t = 2*np.cos(2*theta) / D
    S = A + t*(P - A)
    s_param = 0.5 + 0.5/D
    S_check = Q + s_param*(R - Q)
    assert np.allclose(S, S_check, atol=1e-9)
    def area(v1, v2, v3):
        return 0.5*abs((v2[0]-v1[0])*(v3[1]-v1[1])-(v3[0]-v1[0])*(v2[1]-v1[1]))
    f_theta = area(B, O, Q)
    g_theta = area(P, R, S)
    return g_theta / f_theta

limit_approx = compute_ratio(1e-7)
expected = 6/5
if abs(limit_approx - expected) < 1e-4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')