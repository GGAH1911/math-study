import numpy as np

O = np.array([0.0, 0.0])
A = np.array([-5.0, 0.0])
B = np.array([5.0, 0.0])
C = np.array([3.0, 4.0])
D = np.array([24/5, 7/5])
E = np.array([3/5, 4/5])
r = 5.0

try:
    # 1. C, D on semicircle
    assert abs(np.linalg.norm(C - O) - r) < 1e-9, 'C not on circle'
    assert abs(np.linalg.norm(D - O) - r) < 1e-9, 'D not on circle'
    assert C[1] > 0 and D[1] > 0, 'C,D must be on upper half'

    # 2. E on segment CO (C-E-O collinear)
    lam = np.linalg.norm(E) / np.linalg.norm(C)
    assert np.allclose(E, lam * C, atol=1e-9), 'E not on ray OC'
    assert 0 < lam < 1, 'E not between C and O'

    # 3. E on segment AD
    dAD = D - A
    t = (E[0] - A[0]) / dAD[0]
    assert abs(A[1] + t * dAD[1] - E[1]) < 1e-9, 'E not on line AD'
    assert 0 < t < 1, 'E not between A and D'

    # 4. CE=4, ED=3√2
    CE = np.linalg.norm(C - E)
    ED = np.linalg.norm(E - D)
    assert abs(CE - 4) < 1e-9, f'CE={CE}'
    assert abs(ED - 3*np.sqrt(2)) < 1e-9, f'ED={ED}'

    # 5. angle CEA = 3π/4
    vec_EC = C - E
    vec_EA = A - E
    cos_ang = np.dot(vec_EC, vec_EA) / (np.linalg.norm(vec_EC) * np.linalg.norm(vec_EA))
    ang = np.arccos(np.clip(cos_ang, -1, 1))
    assert abs(ang - 3*np.pi/4) < 1e-9, f'angle={ang}'

    # 6. AC x CD = 20√2
    AC = np.linalg.norm(A - C)
    CD = np.linalg.norm(C - D)
    result = AC * CD
    expected = 20 * np.sqrt(2)
    assert abs(result - expected) < 1e-9, f'AC*CD={result}, expected={expected}'

    print('VERIFY_PASS')
except AssertionError as e:
    print(f'VERIFY_FAIL: {e}')
