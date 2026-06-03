import numpy as np
a, b = 3, 2/3
# 주기 검증
period = 2*np.pi / b
assert abs(period - 3*np.pi) < 1e-9, f'period mismatch: {period}'
# 최댓값·최솟값 차 검증
max_val = a + 1
min_val = -a + 1
diff = max_val - min_val
assert abs(diff - 6) < 1e-9, f'diff mismatch: {diff}'
# a, b 양수 검증
assert a > 0 and b > 0
result = a + b
expected = 11/3
if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')