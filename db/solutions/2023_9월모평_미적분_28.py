import numpy as np

def compute_ratio(theta):
    s = np.sin(theta/2)
    c = np.cos(theta/2)
    A = np.array([1.0, 0.0])
    P = np.array([np.cos(theta), np.sin(theta)])
    C = np.array([np.cos(2*theta), np.sin(2*theta)])
    D = np.array([2*np.cos(theta) - 1, 0.0])
    PA = np.linalg.norm(P - A)
    PC = np.linalg.norm(P - C)
    PD = np.linalg.norm(P - D)
    assert abs(PA - PC) < 1e-9 and abs(PA - PD) < 1e-9, f'PA!=PC or PA!=PD'
    t_E = 2 - 2*np.cos(theta)
    E = D + t_E * np.array([np.cos(theta), np.sin(theta)])
    E_check = A + t_E * (P - A)
    assert np.allclose(E, E_check), 'E not on PA'
    def area(P1, P2, P3):
        v1, v2 = P2 - P1, P3 - P1
        return 0.5 * abs(v1[0]*v2[1] - v1[1]*v2[0])
    f_t = area(C, D, P)
    g_t = area(E, D, A)
    return g_t / (theta**2 * f_t)

ratios = [compute_ratio(t) for t in [0.1, 0.01, 0.001, 0.0001, 0.00001]]
print('ratios:', [round(r,6) for r in ratios])
expected = 0.5
if abs(ratios[-1] - expected) < 0.001:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {ratios[-1]:.6f}, expected {expected}')
