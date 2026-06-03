import numpy as np

# 원기둥: 반지름 3, 높이 3
R = 3; H_cyl = 3

# 좌표 설정
P = np.array([3.0, 0.0, 3.0])       # 윗면 둘레
P_prime = np.array([3.0, 0.0, 0.0]) # P에서 아랫면 수선의 발
O = np.array([0.0, 0.0, 3.0])       # 윗면 중심

# B: 아랫면 둘레, BP'=6
B = np.array([-3.0, 0.0, 0.0])
assert abs(np.linalg.norm(B - P_prime) - 6) < 1e-9, 'BP검증 실패'
assert abs(np.linalg.norm(B[:2]) - R) < 1e-9, 'B 반지름 검증 실패'

# A: 아랫면 둘레, a=1/3, b=4√5/3
a_coord = 1/3
b_coord = 4*np.sqrt(5)/3
A = np.array([a_coord, b_coord, 0.0])
assert abs(np.linalg.norm(A[:2]) - R) < 1e-9, 'A 반지름 검증 실패'

# H: AB 중점
H = (A + B) / 2

# 검증 1: OH⊥AB
OH_vec = H - O
AB_vec = B - A
assert abs(np.dot(OH_vec, AB_vec)) < 1e-9, 'OH⊥AB 실패'

# 검증 2: OH=√13
assert abs(np.linalg.norm(OH_vec) - np.sqrt(13)) < 1e-9, 'OH=√13 실패'

# 검증 3: PA⊥AB
PA_vec = A - P
assert abs(np.dot(PA_vec, AB_vec)) < 1e-9, 'PA⊥AB 실패'

# 넓이 계산
PA_cross_PH = np.cross(A - P, H - P)
area = 0.5 * np.linalg.norm(PA_cross_PH)

expected = 5*np.sqrt(5)/2
if abs(area - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area={area}, expected={expected}')
