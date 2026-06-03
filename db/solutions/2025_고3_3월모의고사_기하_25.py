import math

# 포물선: y^2 = 16x
# 초점 F = (4, 0), 준선 x = -4
F = (4, 0)
p = 4

# 원의 넓이가 25π이므로
area = 25 * math.pi
r = math.sqrt(25)  # r = 5
FP_length = 2 * r  # FP = 10

# 포물선 위의 점 P에서 |PF| = x_0 + p
# x_0 + 4 = 10 → x_0 = 6
x0 = FP_length - p  # x0 = 6

# P는 포물선 위의 점이므로 y_0^2 = 16 * x_0
y0_sq = 16 * x0
y0 = math.sqrt(y0_sq)  # 양수만 고려 (음수는 대칭)

# P의 좌표 확인
P = (x0, y0)

# FP의 길이 확인
FP_check = math.sqrt((P[0] - F[0])**2 + (P[1] - F[1])**2)

# 원의 중심은 F와 P의 중점
center = ((F[0] + P[0]) / 2, (F[1] + P[1]) / 2)

# 원의 중심에서 준선 x = -4까지의 거리
distance_to_directrix = center[0] - (-4)

# 검증
if abs(FP_check - 10) < 1e-9 and abs(distance_to_directrix - 9) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')