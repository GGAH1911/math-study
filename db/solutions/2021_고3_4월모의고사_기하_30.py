import numpy as np
from math import sqrt

# 타원 매개변수
a, b_sq, c = 4, 7, 3

# 점 P의 좌표
x0 = 2/3
y0 = 7*sqrt(5)/6
P = np.array([x0, y0])

# 초점
F = np.array([3, 0])
F_prime = np.array([-3, 0])

# 원의 중심
C = np.array([3/8, 0])

# 검증 1: P가 타원 위에 있는가
ellipse_val = x0**2/16 + y0**2/7
print(f'Ellipse check: {abs(ellipse_val - 1) < 1e-10}')

# 검증 2: PF + PF' = 8
PF = np.linalg.norm(P - F)
PF_prime = np.linalg.norm(P - F_prime)
print(f'PF + PF\' = 8: {abs(PF + PF_prime - 8) < 1e-10}')

# 검증 3: 조건 2PQ = PF
# Q는 직선 F'P 위에 있고 C에서 수직인 점
t_Q = (3 + 3/8) * (x0 + 3) / ((x0+3)**2 + y0**2)
Q = F_prime + t_Q * (P - F_prime)
PQ = np.linalg.norm(P - Q)
print(f'2PQ = PF: {abs(2*PQ - PF) < 1e-10}')

# CP 계산
CP = np.linalg.norm(P - C)
result = 24 * CP

if abs(result - 63) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')