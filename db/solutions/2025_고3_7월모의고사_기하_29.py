import numpy as np
from scipy.optimize import fsolve

# 좌표 설정
O = np.array([0.0, 0.0, 0.0])
B = np.array([-5.0, 0.0, 0.0])
D = np.array([5.0, 0.0, 0.0])
C = np.array([0.0, 5.0, 0.0])
A = np.array([-9/5, -12/5, 4.0])

# 검증 1: 모든 점이 반지름 5인 구 위
assert np.isclose(np.linalg.norm(A), 5), f'|A| = {np.linalg.norm(A)}'
assert np.isclose(np.linalg.norm(B), 5), f'|B| = {np.linalg.norm(B)}'
assert np.isclose(np.linalg.norm(C), 5), f'|C| = {np.linalg.norm(C)}'
assert np.isclose(np.linalg.norm(D), 5), f'|D| = {np.linalg.norm(D)}'

# 검증 2: BD = 10
BD = np.linalg.norm(D - B)
assert np.isclose(BD, 10), f'BD = {BD}'

# 검증 3: BC = CD
BC = np.linalg.norm(C - B)
CD = np.linalg.norm(D - C)
assert np.isclose(BC, CD), f'BC = {BC}, CD = {CD}'

# 검증 4: AC = sqrt(74)
AC = np.linalg.norm(C - A)
assert np.isclose(AC, np.sqrt(74)), f'AC = {AC}'

# 검증 5: AB < AD
AB = np.linalg.norm(B - A)
AD = np.linalg.norm(D - A)
assert AB < AD, f'AB = {AB}, AD = {AD}'

# 검증 6: 직선 OA와 평면 BCD의 각
vec_BC = C - B
vec_BD = D - B
normal_BCD = np.cross(vec_BC, vec_BD)
normal_BCD = normal_BCD / np.linalg.norm(normal_BCD)
sin_theta = abs(np.dot(A, normal_BCD)) / np.linalg.norm(A)
cos_theta = np.sqrt(1 - sin_theta**2)
assert np.isclose(cos_theta, 3/5), f'cos_theta = {cos_theta}'
assert np.isclose(sin_theta, 4/5), f'sin_theta = {sin_theta}'

# 정사영 넓이 계산
vec_AB = B - A
vec_AD = D - A
cross_ABD = np.cross(vec_AB, vec_AD)
area_ABD = 0.5 * np.linalg.norm(cross_ABD)

# 두 평면 법선의 각
normal_ABD = cross_ABD / np.linalg.norm(cross_ABD)
cos_angle = abs(np.dot(normal_ABD, normal_BCD))

# 정사영 넓이
area_proj = area_ABD * cos_angle

assert np.isclose(area_proj, 12), f'Projected area = {area_proj}'
print('VERIFY_PASS')