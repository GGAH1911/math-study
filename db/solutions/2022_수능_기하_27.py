import numpy as np

# Cube ABCD-EFGH, side length 4
A = np.array([0, 0, 4], dtype=float)
D = np.array([0, 4, 4], dtype=float)
E = np.array([0, 0, 0], dtype=float)
G = np.array([4, 4, 0], dtype=float)

# M: midpoint of AD
M = (A + D) / 2  # (0, 2, 4)

# Vectors from M
ME = E - M
MG = G - M

# Area via cross product
cross = np.cross(ME, MG)
area = 0.5 * np.linalg.norm(cross)

if abs(area - 12.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area={area}')
