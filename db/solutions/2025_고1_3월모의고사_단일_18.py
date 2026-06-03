import numpy as np

# Found parameters
l = 3.0
p = 3.0/4
h = np.sqrt(l**2 - p**2)  # 3*sqrt(15)/4
s = np.sqrt(2*l*(l+p))     # sqrt(45/2)
EF = 3*(l+2)/s             # sqrt(10)

# Coordinates
E = np.array([0.0, 0.0])
A = np.array([-l, 0.0])
B = np.array([-(p+l), -h])
D = np.array([EF+2, 0.0])
F = np.array([EF, 0.0])
C = np.array([EF+2-p, -h])

# G on line BE extended past E, |EG|=3
dir_BE = (E - B) / np.linalg.norm(E - B)
G = E + 3 * dir_BE

def ang(v1, v2):
    c = np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    return np.arccos(np.clip(c,-1,1))

passes = []
# 1. Parallelogram: AB vector == DC vector
passes.append(np.allclose(B-A, C-D))
# 2. Angle bisector at B
passes.append(np.isclose(ang(A-B, E-B), ang(C-B, E-B)))
# 3. EG = 3
passes.append(np.isclose(np.linalg.norm(G-E), 3.0))
# 4. FG = 2
passes.append(np.isclose(np.linalg.norm(G-F), 2.0))
# 5. FD = 2
passes.append(np.isclose(np.linalg.norm(F-D), 2.0))
# 6. G on line CF
tx = (G[0]-C[0])/(F[0]-C[0])
ty = (G[1]-C[1])/(F[1]-C[1])
passes.append(np.isclose(tx, ty))
# 7. angle FDC = 2 * angle DCF (original condition)
a_FDC = ang(F-D, C-D)
a_DCF = ang(D-C, F-C)
passes.append(np.isclose(a_FDC, 2*a_DCF))
# 8. EF == sqrt(10)
passes.append(np.isclose(EF, np.sqrt(10)))

if all(passes):
    print('VERIFY_PASS')
else:
    for i,ok in enumerate(passes):
        if not ok: print(f'FAIL check {i}')
    print('VERIFY_FAIL')
