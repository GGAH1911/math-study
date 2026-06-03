import math
from math import log2

a = log2(9)
b = log2(9) / 3

# 무게중심 계산
centroid_x = (0 + 2*a + (-log2(9))) / 3
centroid_y = (-log2(9) + log2(7) + a) / 3

# 주어진 무게중심
expected_x = b
expected_y = log2(7) / 3  # log_8(7) = log_2(7) / 3

# 검증
print('Centroid X:', abs(centroid_x - expected_x) < 1e-10)
print('Centroid Y:', abs(centroid_y - expected_y) < 1e-10)

# 최종 답 검증
result = 2**(a + 3*b)
print('2^(a+3b):', abs(result - 81) < 1e-10)

if abs(centroid_x - expected_x) < 1e-10 and abs(centroid_y - expected_y) < 1e-10 and abs(result - 81) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')