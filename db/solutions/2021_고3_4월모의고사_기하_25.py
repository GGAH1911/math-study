import numpy as np
from numpy import sqrt

# 타원 매개변수
a2, b2 = 36, 12
c2 = a2 - b2
c = sqrt(c2)

# |OP| = 4일 때 P의 좌표 계산
op_len = 4
op_len_sq = 16

# x0^2 + y0^2 = 16을 타원 방정식에 대입
# x0^2/36 + (16-x0^2)/12 = 1
# x0^2/36 - x0^2/12 + 4/3 = 1
# x0^2(1/36 - 1/12) = -1/3
# x0^2(-2/36) = -1/3
# x0^2 = 6

x0_sq = 6.0
y0_sq = op_len_sq - x0_sq  # = 10

# P는 제1사분면이므로
x0 = sqrt(x0_sq)
y0 = sqrt(y0_sq)

# 타원 위의 점인지 확인
ellipse_check = x0**2/a2 + y0**2/b2

# 초점까지의 거리
PF = sqrt((x0 - c)**2 + y0**2)
PF_prime = sqrt((x0 + c)**2 + y0**2)

# Q = -P
QF_prime = sqrt((-x0 + c)**2 + (-y0)**2)

# 둘레 계산
OP = sqrt(x0**2 + y0**2)
PQ = 2 * OP
perimeter = PF_prime + QF_prime + PQ

# 검증
if abs(ellipse_check - 1.0) < 1e-9 and abs(perimeter - 20.0) < 1e-9 and abs(OP - 4.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')