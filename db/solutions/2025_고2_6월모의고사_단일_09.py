import numpy as np

a, b = 2, 2

# 주어진 조건 검증
x1 = np.pi / 4
y1 = a * np.sin(b * x1) + 1
assert abs(y1 - 3) < 1e-10, f'x=π/4에서 y=3이어야 함, 실제: {y1}'

x2 = 5 * np.pi / 4
y2 = a * np.sin(b * x2) + 1
assert abs(y2 - 3) < 1e-10, f'x=5π/4에서 y=3이어야 함, 실제: {y2}'

# 최댓값/최솟값 확인
max_val = a * 1 + 1
min_val = -a + 1
assert max_val == 3, f'최댓값이 3이어야 함, 실제: {max_val}'
assert min_val == -1, f'최솟값이 -1이어야 함, 실제: {min_val}'

# 주기 확인
period = 2 * np.pi / b
assert abs(period - np.pi) < 1e-10, f'주기가 π이어야 함, 실제: {period}'

print('VERIFY_PASS')