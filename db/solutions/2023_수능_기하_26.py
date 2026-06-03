import numpy as np

# 원: (x-2)^2 + (y-6)^2 = 4
# 직선: q = (1+t, 2), t는 임의의 실수

# p를 원 위에서 파라미터화
theta_vals = np.linspace(0, 2*np.pi, 100000)
px = 2 + 2*np.cos(theta_vals)
py = 6 + 2*np.sin(theta_vals)

# 각 p에 대해 y=2 직선까지 최소 거리 (x는 자유이므로 수직 거리)
min_dist_each = py - 2  # py >= 4 > 2 이므로 항상 양수

# 원 위의 점에서의 전체 최솟값
global_min = np.min(min_dist_each)

# 조건 확인: 원 방정식 만족 여부
best_idx = np.argmin(min_dist_each)
px_best = px[best_idx]
py_best = py[best_idx]
circle_check = (px_best - 2)**2 + (py_best - 6)**2  # should be ~4

# 답 검증
tolerance = 1e-4
if abs(global_min - 2.0) < tolerance and abs(circle_check - 4.0) < tolerance:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: min={global_min}, circle_eq={circle_check}')
