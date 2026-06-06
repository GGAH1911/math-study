import numpy as np
from math import sqrt

p = 21
t = 2*p/sqrt(3)

# 점들의 좌표
P = np.array([t**2/(4*p), t])
Q = np.array([-p, t/2 - 2*p**2/t])
y_R = t/2 - 2*p**2/t
R = np.array([y_R**2/(4*p), y_R])
F = np.array([p, 0])

# 1. P가 포물선 위의 점인지 확인
check_P = P[1]**2 - 4*p*P[0]
print(f'P on parabola: {abs(check_P) < 1e-10}')

# 2. R이 포물선 위의 점인지 확인
check_R = R[1]**2 - 4*p*R[0]
print(f'R on parabola: {abs(check_R) < 1e-10}')

# 3. Q가 준선 위의 점인지 확인
check_Q = abs(Q[0] - (-p)) < 1e-10
print(f'Q on directrix: {check_Q}')

# 4. 각도 PRQ가 90도인지 확인
RP = P - R
RQ = Q - R
dot_product = np.dot(RP, RQ)
print(f'Angle PRQ = 90 degrees: {abs(dot_product) < 1e-10}')

# 5. 둘레 계산
PQ = np.linalg.norm(P - Q)
QR = np.linalg.norm(Q - R)
RF = np.linalg.norm(R - F)
FP = np.linalg.norm(F - P)
perimeter = PQ + QR + RF + FP
print(f'Perimeter: {perimeter}')
print(f'Perimeter = 140: {abs(perimeter - 140) < 1e-10}')

if abs(perimeter - 140) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')