import numpy as np

# 구 반지름 sqrt(13), OH1=OH2=2
# P=(3,0,2), Q=(0,3,-2), O=(0,0,0)
O = np.array([0.0, 0.0, 0.0])
P = np.array([3.0, 0.0, 2.0])
Q = np.array([0.0, 3.0, -2.0])

# P, Q 구 위 확인
assert abs(np.linalg.norm(P)**2 - 13) < 1e-10
assert abs(np.linalg.norm(Q)**2 - 13) < 1e-10

# 정사영 넓이 계산 (O의 정사영=H2=(0,0,-2), P의 정사영=P'=(3,0,-2), Q 자체)
H2 = np.array([0.0, 0.0, -2.0])
P_proj = np.array([P[0], P[1], -2.0])
H2P = P_proj - H2
H2Q = Q - H2
cross_proj = np.cross(H2P, H2Q)
area_proj = 0.5 * np.linalg.norm(cross_proj)  # 9/2

# 삼각형 POQ 넓이
OP = P - O
OQ = Q - O
cross_OPQ = np.cross(OP, OQ)
area_OPQ = 0.5 * np.linalg.norm(cross_OPQ)  # 3*sqrt(17)/2

cos_theta = area_proj / area_OPQ
expected = 3 * np.sqrt(17) / 17

# 정사영 넓이가 최대 9/2인지 확인
assert abs(area_proj - 9/2) < 1e-10

if abs(cos_theta - expected) < 1e-8:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {cos_theta:.10f}, expected {expected:.10f}')
