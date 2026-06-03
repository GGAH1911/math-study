import numpy as np

alpha = 1/4
x_A = alpha
x_B = 2 - alpha
x_C = 4 + alpha

k = np.sin(np.pi / 2 * x_A)
tol = 1e-9

# 모든 점이 원래 곡선 y = sin(pi/2 * x) 위에 있는지 확인
assert abs(np.sin(np.pi/2 * x_A) - k) < tol, 'A not on curve'
assert abs(np.sin(np.pi/2 * x_B) - k) < tol, 'B not on curve'
assert abs(np.sin(np.pi/2 * x_C) - k) < tol, 'C not on curve'

# x 좌표 합 조건 확인
assert abs(x_A + x_B + x_C - 25/4) < tol, 'Sum not 25/4'

# 0 < k < 1 확인
assert 0 < k < 1, 'k not in (0,1)'

# AB 길이 확인 (A, B 모두 y=k 위의 점)
AB = x_B - x_A
expected = 3/2

if abs(AB - expected) < tol:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
