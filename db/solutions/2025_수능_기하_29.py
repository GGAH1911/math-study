import numpy as np
from scipy.optimize import fsolve

# 쌍곡선: x^2 - y^2/35 = 1
def hyperbola(x, y):
    return x**2 - y**2/35 - 1

# P 좌표
P = np.array([4/3, 7*np.sqrt(5)/3])
F = np.array([6, 0])
F_prime = np.array([-6, 0])

# P가 쌍곡선 위에 있는지 확인
hyp_check = hyperbola(P[0], P[1])

# PF, PF' 거리
PF = np.linalg.norm(P - F)
PF_prime = np.linalg.norm(P - F_prime)

# 쌍곡선 조건 확인
hyperbola_condition = PF_prime - PF

# Q 계산
direction = P - F_prime
direction_normalized = direction / np.linalg.norm(direction)
Q = P + 7 * direction_normalized

# F'Q 거리
F_prime_Q = np.linalg.norm(Q - F_prime)

# 닮음 조건 확인
FF_prime = 12
nullable_product = F_prime_Q * PF_prime
expected_product = FF_prime ** 2

# 넓이 계산
def triangle_area(p1, p2, p3):
    return 0.5 * abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1]))

area_PFQ = triangle_area(P, F, Q)
area_ratio = area_PFQ / np.sqrt(5)

# 검증
if abs(hyp_check) < 1e-10 and abs(hyperbola_condition - 2) < 1e-10 and abs(nullable_product - expected_product) < 1e-10 and PF < F_prime_Q:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')