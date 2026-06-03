import numpy as np

c = -np.cos(np.pi / 8)
k_ans = 11 * np.pi / 8

# 1) k = 11pi/8 일 때 sin(k) = c 이므로 x=k는 해 아님 (엄격 부등호)
assert abs(np.sin(k_ans) + np.cos(np.pi / 8)) < 1e-9, 'sin(11pi/8) should equal c'

# 2) [-pi, k] 에서 sin x + cos(pi/8) < 0 의 해집합이 (-5pi/8, -3pi/8) 인지 확인
x = np.linspace(-np.pi, k_ans, 200000)
sol = x[np.sin(x) + np.cos(np.pi / 8) < 0]
assert len(sol) > 0, 'no solutions found'
assert abs(sol.min() - (-5*np.pi/8)) < 0.0001, f'left endpoint mismatch: {sol.min()}'
assert abs(sol.max() - (-3*np.pi/8)) < 0.0001, f'right endpoint mismatch: {sol.max()}'

# 3) 해집합이 단일 구간인지 (갭 없음)
gaps = np.where(np.diff(sol) > 0.01)[0]
assert len(gaps) == 0, f'expected 1 interval, got gap at idx {gaps}'

# 4) alpha = -3pi/8 로 (-pi-alpha, alpha) 형태 확인
alpha = -3 * np.pi / 8
assert abs(-np.pi - alpha - (-5*np.pi/8)) < 1e-9
assert abs(alpha - (-3*np.pi/8)) < 1e-9

# 5) k > 11pi/8 이면 두 번째 구간 등장 확인
k_over = 11*np.pi/8 + 0.05
x2 = np.linspace(-np.pi, k_over, 200000)
sol2 = x2[np.sin(x2) + np.cos(np.pi/8) < 0]
gaps2 = np.where(np.diff(sol2) > 0.01)[0]
assert len(gaps2) >= 1, 'expected 2 intervals for k > 11pi/8'

print('VERIFY_PASS')