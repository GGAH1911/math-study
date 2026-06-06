import numpy as np
from scipy.spatial.distance import cdist

# 삼각형 AOB의 꼭짓점
A = np.array([0, 8])
O = np.array([0, 0])
B = np.array([8, 0])

# 삼각형 CDB의 꼭짓점
C = np.array([7, 1])
D = np.array([7, 0])
B_tri = np.array([8, 0])

# OE 벡터
OE = np.array([-4, 2])

# 검증 점들
P_test = np.array([4, 4])  # 변 AB 위의 점
Q_test = np.array([7, 1])  # 점 C

# PQ 벡터
PQ = Q_test - P_test
# PQ + OE
vec = PQ + OE
# 거리의 제곱
dist_sq_min = np.sum(vec**2)

print(f"최솟값 검증: |PQ + OE|² = {dist_sq_min}")
assert dist_sq_min == 2, f"Expected 2, got {dist_sq_min}"

# 최댓값 검증
P_test_max = np.array([0, 8])  # 점 A
Q_test_max = np.array([8, 0])  # 점 B

PQ_max = Q_test_max - P_test_max
vec_max = PQ_max + OE
dist_sq_max = np.sum(vec_max**2)

print(f"최댓값 검증: |PQ + OE|² = {dist_sq_max}")
assert dist_sq_max == 52, f"Expected 52, got {dist_sq_max}"

M = 52
m = 2
result = M + m
print(f"M + m = {result}")
assert result == 54
print("VERIFY_PASS")