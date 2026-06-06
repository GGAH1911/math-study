import numpy as np
from scipy.optimize import fsolve

h_squared = 59/4
h = np.sqrt(h_squared)

# 좌표
A = np.array([0, 0])
B = np.array([2, 0])
C = np.array([0.5, h])
D = np.array([3, 2*h])

# 삼각형 ABC
AC = np.linalg.norm(C - A)
BC = np.linalg.norm(C - B)
AB = 2
area_ABC = h
r = (AB * AC * BC) / (4 * area_ABC)

# 삼각형 ABD
AD = np.linalg.norm(D - A)
BD = np.linalg.norm(D - B)
area_ABD = 2*h
R = (AB * AD * BD) / (4 * area_ABD)

# 각도
cos_CAB = np.dot(C - A, B - A) / (AC * AB)
sin_CAB = np.sqrt(1 - cos_CAB**2)

# 검증
result = 4 * (R**2 - r**2) * (sin_CAB**2)
AC_squared = AC**2

if abs(result - 51) < 1e-9 and abs(AC_squared - 15) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: result={result}, AC_squared={AC_squared}')