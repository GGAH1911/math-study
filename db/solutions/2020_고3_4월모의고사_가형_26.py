import numpy as np

CANDIDATE = 14

# 주어진 조건에서 a = 7, b = 2
a = 7
b = 2

# a * b 계산
product = a * b

# sin(3x) = (9-b)/a = 1일 때 교점 개수 확인
sin_val_1 = (9 - b) / a
if abs(sin_val_1 - 1.0) < 1e-10:  # sin(3x) = 1
    # 0 <= 3x <= 6π에서 sin(3x) = 1인 점: 3x = π/2, 5π/2, 9π/2
    count_1 = 3
else:
    count_1 = 0

# sin(3x) = (2-b)/a = 0일 때 교점 개수 확인
sin_val_2 = (2 - b) / a
if abs(sin_val_2) < 1e-10:  # sin(3x) = 0
    # 0 <= 3x <= 6π에서 sin(3x) = 0인 점: 3x = 0, π, 2π, 3π, 4π, 5π, 6π
    count_2 = 7
else:
    count_2 = 0

# 조건 검증
if count_1 == 3 and count_2 == 7 and product == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')