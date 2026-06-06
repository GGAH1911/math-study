import numpy as np
from math import sqrt

# 두 원의 중심
O1 = np.array([0, -4])
O2 = np.array([0, 1])

# 반지름 계산
r1 = sqrt((O1[0] - 2)**2 + (O1[1] - 0)**2)
r2 = sqrt((O2[0] - 2)**2 + (O2[1] - 0)**2)

# 직선까지의 거리 함수
def dist_to_line1(a, b):
    return abs(2*a - b + 6) / sqrt(5)

def dist_to_line2(a, b):
    return abs(2*a + b - 6) / sqrt(5)

# O1 검증
print(f"O1 점(2,0) 지남: {abs(r1 - sqrt(20)) < 1e-10}")
print(f"O1 L1 접함: {abs(dist_to_line1(O1[0], O1[1]) - r1) < 1e-10}")
print(f"O1 L2 접함: {abs(dist_to_line2(O1[0], O1[1]) - r1) < 1e-10}")

# O2 검증
print(f"O2 점(2,0) 지남: {abs(r2 - sqrt(5)) < 1e-10}")
print(f"O2 L1 접함: {abs(dist_to_line1(O2[0], O2[1]) - r2) < 1e-10}")
print(f"O2 L2 접함: {abs(dist_to_line2(O2[0], O2[1]) - r2) < 1e-10}")

# 최종 답
answer = np.linalg.norm(O2 - O1)
if abs(answer - 5) < 1e-10:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")