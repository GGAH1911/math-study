import numpy as np
a, b, c = 2, 0.5, 3
# 조건 1: x=π에서 최댓값 5
y_at_pi = a * np.sin(b * np.pi) + c
assert np.isclose(y_at_pi, 5), f'x=π에서 y={y_at_pi}, 예상=5'
# 조건 2: x=3π에서 최솟값 1
y_at_3pi = a * np.sin(b * 3 * np.pi) + c
assert np.isclose(y_at_3pi, 1), f'x=3π에서 y={y_at_3pi}, 예상=1'
# 조건 3: 최댓값이 5
max_y = a + c
assert max_y == 5, f'최댓값={max_y}, 예상=5'
# 조건 4: 최솟값이 1
min_y = -a + c
assert min_y == 1, f'최솟값={min_y}, 예상=1'
# 조건 5: a, b, c 곱
product = a * b * c
assert product == 3, f'곱={product}, 예상=3'
print('VERIFY_PASS')