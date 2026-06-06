import math
k_squared = 2
k = math.sqrt(k_squared)
sqrt_term = math.sqrt(k_squared + 1)

# 점 A, B의 좌표
A_x = -1 / sqrt_term
A_y = k / sqrt_term
B_x = k / sqrt_term
B_y = -1 / sqrt_term

# 각도 구하기 (동경)
cos_alpha = A_x / math.sqrt(A_x**2 + A_y**2)
sin_alpha = A_y / math.sqrt(A_x**2 + A_y**2)
cos_beta = B_x / math.sqrt(B_x**2 + B_y**2)
sin_beta = B_y / math.sqrt(B_x**2 + B_y**2)

# 검증
result = cos_alpha * sin_beta
expected = 1/3

if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')