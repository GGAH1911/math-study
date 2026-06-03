import numpy as np

sqrt2 = np.sqrt(2)
H = np.array([0.0, 0.0, 0.0])
A = np.array([sqrt2, 0.0, 0.0])
B = np.array([0.0, 2.0, 0.0])
C = np.array([0.0, 0.0, 1.0])

# (가) AHB = pi/2
HA = A - H
HB = B - H
cos_AHB = np.dot(HA, HB) / (np.linalg.norm(HA) * np.linalg.norm(HB))
assert abs(cos_AHB) < 1e-10, f'AHB fail: {cos_AHB}'

# (나) sin(CAH)
AC = C - A
AH_v = H - A
cos_CAH = np.dot(AC, AH_v) / (np.linalg.norm(AC) * np.linalg.norm(AH_v))
sin_CAH = np.sqrt(max(0.0, 1 - cos_CAH**2))
expected = np.sqrt(3) / 3
assert abs(sin_CAH - expected) < 1e-9, f'sin(CAH) fail: {sin_CAH}'

# (나) sin(ABH)
BA = A - B
BH_v = H - B
cos_ABH = np.dot(BA, BH_v) / (np.linalg.norm(BA) * np.linalg.norm(BH_v))
sin_ABH = np.sqrt(max(0.0, 1 - cos_ABH**2))
assert abs(sin_ABH - expected) < 1e-9, f'sin(ABH) fail: {sin_ABH}'

# H not on AB: parameterize AB and check
# If H = A + t*(B-A), then t_x: 0=sqrt2+t*(-sqrt2)->t=1; t_y: 0=0+t*2->t=0. Contradiction.
AB_vec = B - A
if np.linalg.norm(AB_vec[:2]) > 1e-10:
    t_candidates = [(H[i] - A[i]) / AB_vec[i] for i in range(2) if abs(AB_vec[i]) > 1e-10]
    assert len(set(round(t, 6) for t in t_candidates)) > 1, 'H on AB fail'

# cos(theta): angle between plane ABC and plane alpha
n1 = np.array([0.0, 0.0, 1.0])
n2 = np.cross(AB_vec, AC)
cos_theta = abs(np.dot(n1, n2)) / (np.linalg.norm(n1) * np.linalg.norm(n2))
expected_cos = 2 * np.sqrt(7) / 7

if abs(cos_theta - expected_cos) < 1e-8:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {cos_theta:.10f}, expected {expected_cos:.10f}')
