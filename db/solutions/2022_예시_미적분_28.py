import numpy as np

def compute_ratio(theta):
    # A=(0,0), B=(2,0), semicircle center (1,0) radius 1
    px = 1 + np.cos(2*theta)
    py = np.sin(2*theta)
    AP = 2 * np.cos(theta)
    # Law of sines: AQ
    AQ = AP * np.sin(theta/3) / np.sin(4*theta/3)
    # Verify angle at P is theta/3
    P = np.array([px, py])
    A = np.array([0.0, 0.0])
    B = np.array([2.0, 0.0])
    Q = np.array([AQ, 0.0])
    PA = A - P
    PQ_vec = Q - P
    cos_angle_P = np.dot(PA, PQ_vec) / (np.linalg.norm(PA) * np.linalg.norm(PQ_vec))
    angle_at_P = np.arccos(np.clip(cos_angle_P, -1, 1))
    angle_err = abs(angle_at_P - theta/3)
    # S(theta)
    S = 0.5 * AQ * py
    # l(theta)
    l = np.linalg.norm(B - P)
    return S / l, angle_err

all_pass = True
for eps in [1e-3, 1e-4, 1e-5, 1e-6]:
    ratio, angle_err = compute_ratio(eps)
    if abs(ratio - 0.25) > 0.005:
        all_pass = False
        break
    if angle_err > 1e-9:
        all_pass = False
        break

print('VERIFY_PASS' if all_pass else 'VERIFY_FAIL')
