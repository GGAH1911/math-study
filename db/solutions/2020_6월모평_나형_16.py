import math
from itertools import product

# 모든 경우의 수 (a, b, c, d)
valid_count = 0
for a, b, c, d in product(range(1, 7), repeat=4):
    if a * b * c * d == 12:
        valid_count += 1

total = 6**4
prob = valid_count / total

# 검증: 1/36인지 확인
expected = 1/36
if abs(prob - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')