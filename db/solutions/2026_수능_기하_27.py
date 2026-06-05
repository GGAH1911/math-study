import numpy as np

h = np.sqrt(21)
A = np.array([-2.5, 0, 0], dtype=float)
B = np.array([2.5, 0, 0], dtype=float)
C = np.array([-1.5, 2, h], dtype=float)
D = np.array([1.5, 2, h], dtype=float)
H = np.array([1.5, 2, 0], dtype=float)

# Verify AB = 5
assert np.isclose(np.linalg.norm(B - A), 5)
# Verify CD = 3
assert np.isclose(np.linalg.norm(D - C), 3)
# Verify AD = BC
assert np.isclose(np.linalg.norm(D - A), np.linalg.norm(C - B))

# Area ABCD
vec_AB = B - A
vec_AC = C - A
vec_AD = D - A
area_ABC = 0.5 * np.linalg.norm(np.cross(vec_AB, vec_AC))
area_ACD = 0.5 * np.linalg.norm(np.cross(vec_AC, vec_AD))
area_ABCD = area_ABC + area_ACD

# Area ABH
vec_AH = H - A
area_ABH = 0.5 * np.linalg.norm(np.cross(vec_AB, vec_AH))

# Check main condition
if np.isclose(area_ABCD, 4 * area_ABH):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')