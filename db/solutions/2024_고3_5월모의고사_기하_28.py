import numpy as np

# 원래 조건
# l1: y=0, l2: y=d (d=4)
d = 4
# A on l1, B on l2, |AB|=5
A = np.array([0.0, 0.0])
# b^2 + d^2 = 25 => b = 3
b = 3.0
B = np.array([b, d])
AB = B - A
assert abs(np.linalg.norm(AB) - 5.0) < 1e-9, 'VERIFY_FAIL: |AB|!=5'

# 최솟값 조건: e_x - c_x = 4b = 12
# C=(0,0), D=(12,4)
C = np.array([0.0, 0.0])
Dpt = np.array([4*b, d])
CD = Dpt - C

# |4AB - CD| 계산
val = np.linalg.norm(4*AB - CD)
assert abs(val - 12.0) < 1e-9, f'VERIFY_FAIL: min value = {val}'

# k = |CD|
k = np.linalg.norm(CD)
assert abs(k - 4*np.sqrt(10)) < 1e-9, f'VERIFY_FAIL: k = {k}'

# d*k
result = d * k
expected = 16 * np.sqrt(10)
assert abs(result - expected) < 1e-9, f'VERIFY_FAIL: d*k = {result}'

print('VERIFY_PASS')
