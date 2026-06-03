import numpy as np

# 원래 조건 직접 사용
# p: 직선 x=1 위의 점 (1, t)
# q: 원 중심 (4,2) 반지름 1 위의 점 (4+cos(theta), 2+sin(theta))

min_dist = float('inf')
theta_vals = np.linspace(0, 2*np.pi, 100000)

for theta in theta_vals:
    qx = 4 + np.cos(theta)
    qy = 2 + np.sin(theta)
    # p의 y는 자유, qy와 같게 놓으면 x방향 거리만 남음
    # |p - q|^2 = (1 - qx)^2 + (t - qy)^2, t=qy로 최소화
    dist = abs(1 - qx)
    if dist < min_dist:
        min_dist = dist

# 검증: 조건 확인
p_opt = np.array([1.0, 2.0])
q_opt = np.array([3.0, 2.0])

cond1 = np.dot(p_opt, np.array([3, 0]))  # p·a = 3?
cond2 = np.linalg.norm(q_opt - np.array([4, 2]))  # |q - c| = 1?
dist_pq = np.linalg.norm(p_opt - q_opt)

if abs(cond1 - 3) < 1e-9 and abs(cond2 - 1) < 1e-9 and abs(dist_pq - 2) < 1e-6 and abs(min_dist - 2) < 1e-4:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: cond1={cond1}, cond2={cond2}, dist={dist_pq}, min_dist={min_dist}')