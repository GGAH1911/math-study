import numpy as np

# 주어진 점들
A = np.array([-2.0, 0.0])
B = np.array([0.0, 4.0])
a, b = 2.0, 0.5
C = np.array([a, b])

# 조건 1: 무게중심이 y축 위에 있는가?
centroid = (A + B + C) / 3
if not np.isclose(centroid[0], 0):
    print('VERIFY_FAIL')
    exit()

# 조건 2: AC = BC인가?
AC = np.linalg.norm(C - A)
BC = np.linalg.norm(C - B)
if not np.isclose(AC, BC):
    print('VERIFY_FAIL')
    exit()

# 최종 답 검증
if np.isclose(a + b, 2.5):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')