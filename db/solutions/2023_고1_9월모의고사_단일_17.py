import numpy as np

# 원래 문제 조건으로 좌표 설정
A = np.array([0.0, 4.0])
B = np.array([0.0, 0.0])
C = np.array([8.0, 0.0])

# d=3 결정 (수직 조건)
d = 3.0
D = np.array([d, 4.0])
P = A + (2/3)*(D - A)  # 2:1 내분

# 직선 AC, BP의 기울기 수직 확인
slope_AC = (C[1]-A[1])/(C[0]-A[0])
slope_BP = (P[1]-B[1])/(P[0]-B[0])
assert abs(slope_AC * slope_BP + 1) < 1e-9, 'VERIFY_FAIL: 수직 조건 불만족'

# 교점 Q 계산: AC: x+2y=8, BP: y=2x
# x+4x=8 -> x=8/5
Qx = 8/5
Qy = 2*Qx
Q = np.array([Qx, Qy])

# Q가 직선 AC 위에 있는지 확인
assert abs(Q[0] + 2*Q[1] - 8) < 1e-9, 'VERIFY_FAIL: Q not on AC'
# Q가 직선 BP 위에 있는지 확인 (y=2x)
assert abs(Q[1] - 2*Q[0]) < 1e-9, 'VERIFY_FAIL: Q not on BP'

# 삼각형 AQD 넓이
def triangle_area(P1, P2, P3):
    return 0.5 * abs((P2[0]-P1[0])*(P3[1]-P1[1]) - (P3[0]-P1[0])*(P2[1]-P1[1]))

area = triangle_area(A, Q, D)
expected = 6/5
assert abs(area - expected) < 1e-9, f'VERIFY_FAIL: area={area}, expected={expected}'
print('VERIFY_PASS')
