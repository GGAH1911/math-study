import numpy as np
k = 1/2
A = np.array([0, 1])
B = np.array([0, 0])
C = np.array([1, 0])
D = np.array([1, 1])
AB = B - A
BC = C - B
AC = C - A
CD = D - C
v1 = AB + k * BC
v2 = AC + 3*k * CD
dot = np.dot(v1, v2)
if abs(dot) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', dot)
