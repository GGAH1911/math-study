import numpy as np

# 원 C: x^2 + (y-2)^2 = 4, center=(0,2), r=2
# A(2,-2), B(5,1), P 는 원 위의 점
# 직선 AB: x - y - 4 = 0

# 답: P = (-sqrt(2), 2+sqrt(2))
px = -np.sqrt(2)
py = 2 + np.sqrt(2)

# 1. P가 원 위에 있는지 확인
on_circle = np.isclose(px**2 + py**2 - 4*py, 0, atol=1e-9)

# 2. 원의 모든 점 중 이 P의 거리가 최대인지 확인
# 원 위 임의 점 P(t) = (2cos(t), 2+2sin(t))
t_vals = np.linspace(0, 2*np.pi, 100000)
ptx = 2*np.cos(t_vals)
pty = 2 + 2*np.sin(t_vals)
dists = np.abs(ptx - pty - 4) / np.sqrt(2)
max_dist = np.max(dists)

# 답의 점에서 거리
ans_dist = np.abs(px - py - 4) / np.sqrt(2)

# 3. 삼각형 넓이 계산
A = np.array([2, -2])
B = np.array([5, 1])
P = np.array([px, py])
AB = np.linalg.norm(B - A)
area_ans = 0.5 * AB * ans_dist

# 각 t 에서 넓이
areas = 0.5 * AB * dists
max_area = np.max(areas)

if on_circle and np.isclose(ans_dist, max_dist, atol=1e-6) and np.isclose(area_ans, max_area, atol=1e-6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'on_circle={on_circle}, ans_dist={ans_dist:.6f}, max_dist={max_dist:.6f}')
