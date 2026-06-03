import math

# 주어진 조건
BC = 5
angle_A = math.pi / 6
angle_B = math.pi / 4

# AC 계산 (내 답)
AC = 5 * math.sqrt(2)

# 사인 법칙으로 검증: BC/sin(A) = AC/sin(B)
lhs = BC / math.sin(angle_A)
rhs = AC / math.sin(angle_B)

if abs(lhs - rhs) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')