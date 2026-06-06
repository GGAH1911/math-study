import numpy as np
from scipy.optimize import minimize_scalar

# 점 P의 좌표 (선분 OA를 2:1로 외분)
P = np.array([2, 4])

# 점 A, B
A = np.array([1, 2])
B = np.array([5, 5])

# Q는 선분 AB 위의 점: Q = A + t(B - A), 0 <= t <= 1
def PQ_squared(t):
    Q = A + t * (B - A)
    return np.sum((Q - P)**2)

# 최솟값과 최댓값 찾기
result_min = minimize_scalar(PQ_squared, bounds=(0, 1), method='bounded')
t_min = result_min.x
m = result_min.fun

# 경계값 확인
M_candidate_0 = PQ_squared(0)
M_candidate_1 = PQ_squared(1)
M = max(M_candidate_0, M_candidate_1)

# 정답 확인
M_plus_m = M + m

# 검증
if abs(m - 1.0) < 1e-6 and abs(M - 10.0) < 1e-6 and abs(M_plus_m - 11.0) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')