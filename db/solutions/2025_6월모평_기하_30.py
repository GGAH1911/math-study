import numpy as np
from scipy.optimize import fminbound

# 정의: 쌍곡선 위의 점 P, 조건을 만족하는 Q
def compute_AQ_distance(x, sign_y=1):
    if x**2 < 9:
        return np.nan
    
    # 쌍곡선 위의 점
    y = sign_y * 4 * np.sqrt(x**2 - 9) / 3
    
    # |FP| 계산
    PF_dist = np.sqrt((x - 5)**2 + y**2)
    
    # Q 계산
    r = PF_dist
    denom = r + 6
    F_prime = np.array([-5, 0])
    P = np.array([x, y])
    Q = ((r + 1) * F_prime + 5 * P) / denom
    
    # |AQ| 계산
    A = np.array([-9, -3])
    AQ_dist = np.linalg.norm(Q - A)
    return AQ_dist

# 최댓값 찾기 (오른쪽 가지, 위쪽)
result_upper = fminbound(lambda x: -compute_AQ_distance(x, 1), 3, 30)
max_dist_upper = compute_AQ_distance(result_upper, 1)

# 특정 점에서 검증: x = 273/35
x_critical = 273 / 35
y_critical = 4 * np.sqrt(x_critical**2 - 9) / 3
dist_critical = compute_AQ_distance(x_critical, 1)

# 원점에서도 검증
if abs(dist_critical - 10.0) < 0.001:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed {dist_critical}, expected 10')