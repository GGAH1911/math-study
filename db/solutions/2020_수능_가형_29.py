import numpy as np
from scipy.linalg import det
import sympy as sp

CANDIDATE = 29

# 좌표
A = np.array([3, -3, 3], dtype=float)
B = np.array([-2, 7, -2], dtype=float)
C = (1/3) * np.array([1 - np.sqrt(3), 1, 1 + np.sqrt(3)], dtype=float)
D = (1/3) * np.array([1 + np.sqrt(3), 1, 1 - np.sqrt(3)], dtype=float)

# C, D가 단위 구 위에 있는지 확인
assert abs(np.linalg.norm(C) - 1.0) < 1e-10, f"C가 단위 구 위에 없음: {np.linalg.norm(C)}"
assert abs(np.linalg.norm(D) - 1.0) < 1e-10, f"D가 단위 구 위에 없음: {np.linalg.norm(D)}"

# 벡터들
AB = B - A
AC = C - A
AD = D - A

# 행렬식으로 부피 계산
matrix = np.array([AB, AC, AD])
volume_scaled = abs(np.linalg.det(matrix)) / 6

# 부피는 (20/9)*sqrt(3) 형태
sqrt3 = np.sqrt(3)
volume_expected = (20/9) * sqrt3

if abs(volume_scaled - volume_expected) < 1e-10:
    p, q = 9, 20
    answer = p + q
    if answer == CANDIDATE:
        print("VERIFY_PASS")
    else:
        print(f"VERIFY_FAIL: 부피는 맞지만 답이 다름 {answer} vs {CANDIDATE}")
else:
    print(f"VERIFY_FAIL: 부피 불일치 {volume_scaled} vs {volume_expected}")