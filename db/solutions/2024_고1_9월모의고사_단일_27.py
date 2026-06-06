import numpy as np

a_squared = 32
a = np.sqrt(a_squared)

A = np.array([a, 2])
B = np.array([2, a])
C = np.array([2, -a])
O = np.array([0, 0])

def circumradius(p1, p2, p3):
    side_a = np.linalg.norm(p2 - p3)
    side_b = np.linalg.norm(p3 - p1)
    side_c = np.linalg.norm(p1 - p2)
    area = 0.5 * abs(np.cross(p2 - p1, p3 - p1))
    return (side_a * side_b * side_c) / (4 * area)

r1 = circumradius(A, B, C)
r2 = circumradius(A, O, C)
product = r1 * r2
expected = 18 * np.sqrt(2)

if np.isclose(product, expected, rtol=1e-10):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')