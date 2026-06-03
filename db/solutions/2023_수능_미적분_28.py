import numpy as np

def f(theta):
    return 0.5 * np.sin(2*theta)

def g(theta):
    a = 2*theta
    C = np.array([0.0, 1.0])
    Q = np.array([-np.sin(a), np.cos(a)])
    R = np.array([(-1 + np.cos(a) - np.sin(a)) / 2,
                  (np.sin(a) + np.cos(a) - 1) / 2])
    S = np.array([0.0, np.tan(theta)])
    verts = [C, Q, R, S]
    area = 0.0
    n = len(verts)
    for i in range(n):
        j = (i + 1) % n
        area += verts[i][0] * verts[j][1] - verts[j][0] * verts[i][1]
    return abs(area) / 2

# 1) PB == QC 검증
for theta in [0.2, 0.5, 0.7]:
    a = 2*theta
    P = np.array([np.cos(a), np.sin(a)])
    B = np.array([1.0, 0.0])
    Q = np.array([-np.sin(a), np.cos(a)])
    C = np.array([0.0, 1.0])
    assert abs(np.linalg.norm(P-B) - np.linalg.norm(Q-C)) < 1e-12

# 2) angle CQR == pi/2 검증
for theta in [0.2, 0.5, 0.7]:
    a = 2*theta
    Q = np.array([-np.sin(a), np.cos(a)])
    C = np.array([0.0, 1.0])
    R = np.array([(-1 + np.cos(a) - np.sin(a)) / 2,
                  (np.sin(a) + np.cos(a) - 1) / 2])
    QC = C - Q; QR = R - Q
    assert abs(np.dot(QC, QR)) < 1e-12

# 3) 극한 수치 확인
limit_vals = []
for theta in [1e-4, 1e-5, 1e-6, 1e-7]:
    val = (3*f(theta) - 2*g(theta)) / theta**2
    limit_vals.append(val)

if all(abs(v - 2) < 0.01 for v in limit_vals):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', limit_vals)
