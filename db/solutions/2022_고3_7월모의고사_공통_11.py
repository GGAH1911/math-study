import math

# A와 B의 좌표
x_A, y_A = 4, 3
x_B, y_B = 8, 5

# 곡선 위의 점 확인
y_A_check = math.log2(2 * x_A)
y_B_check = math.log2(4 * x_B)

assert abs(y_A - y_A_check) < 1e-9, f'A point check failed: {y_A} vs {y_A_check}'
assert abs(y_B - y_B_check) < 1e-9, f'B point check failed: {y_B} vs {y_B_check}'

# AB 거리 확인
dist_AB = math.sqrt((x_B - x_A)**2 + (y_B - y_A)**2)
expected_dist = 2 * math.sqrt(5)
assert abs(dist_AB - expected_dist) < 1e-9, f'Distance check failed: {dist_AB} vs {expected_dist}'

# 직선의 기울기 확인 (1/2)
slope = (y_B - y_A) / (x_B - x_A)
assert abs(slope - 0.5) < 1e-9, f'Slope check failed: {slope}'

# 삼각형 넓이: C=(4,0), A=(4,3), B=(8,5)
# AC는 수직선(길이 3), B와 AC 사이의 거리(수평거리) = |x_B - x_A| = 4
area = 0.5 * 3 * 4
print('VERIFY_PASS' if abs(area - 6) < 1e-9 else 'VERIFY_FAIL')