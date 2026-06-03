import math

# 원점에서 점 A(a, 3)까지의 거리
# OA = 4 조건에서 a^2 구하기

# a^2 + 9 = 16 (OA=4를 제곱)
# a^2 = 7

a_squared = 7

# 검증: OA = sqrt(a^2 + 9) = 4인지 확인
OA = math.sqrt(a_squared + 9)

if abs(OA - 4.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')