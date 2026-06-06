import numpy as np
from numpy.linalg import norm

# 좌표 설정
A = np.array([0, 3, 6*np.sqrt(2)])
B = np.array([3*np.sqrt(3), 0, 0])
C = np.array([-3*np.sqrt(3), 0, 0])
D = np.array([0, 9, 0])
O = np.array([0, 3, 0])  # 구의 중심

# 반지름 확인
radius = norm(B - O)
assert abs(radius - 6) < 1e-10, f"반지름 오류: {radius}"

# P, Q, R 구하기 (선분과 구의 교점)
def find_intersection(A, endpoint, O, r):
    """선분 A-endpoint와 구의 교점 중 endpoint가 아닌 점"""
    direction = endpoint - A
    # |A + t*direction - O|^2 = r^2
    # |A - O|^2 + 2t*(A-O)·direction + t^2|direction|^2 = r^2
    AO = A - O
    a_coef = np.dot(direction, direction)
    b_coef = 2 * np.dot(AO, direction)
    c_coef = np.dot(AO, AO) - r**2
    
    discriminant = b_coef**2 - 4*a_coef*c_coef
    t1 = (-b_coef + np.sqrt(discriminant)) / (2*a_coef)
    t2 = (-b_coef - np.sqrt(discriminant)) / (2*a_coef)
    
    # t=1에 가까운 것이 endpoint
    if abs(t1 - 1) < abs(t2 - 1):
        return A + t2 * direction
    else:
        return A + t1 * direction

P = find_intersection(A, B, O, 6)
Q = find_intersection(A, C, O, 6)
R = find_intersection(A, D, O, 6)

# P, Q, R이 구 위에 있는지 확인
assert abs(norm(P - O) - 6) < 1e-10, f"P가 구 위에 없음"
assert abs(norm(Q - O) - 6) < 1e-10, f"Q가 구 위에 없음"
assert abs(norm(R - O) - 6) < 1e-10, f"R이 구 위에 없음"

# 삼각형 PQR의 넓이
PQ = Q - P
PR = R - P
cross_product = np.cross(PQ, PR)
area_PQR = 0.5 * norm(cross_product)

# 접평면의 법선 벡터 (OP 방향)
normal_tangent = P - O
normal_tangent = normal_tangent / norm(normal_tangent)

# PQR의 법선 벡터 (z 방향)
normal_PQR = np.array([0, 0, 1])

# 정사영 넓이
cos_theta = abs(np.dot(normal_tangent, normal_PQR))
projected_area = area_PQR * cos_theta
k_squared = projected_area**2

if abs(k_squared - 24) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: k^2 = {k_squared}, expected 24')