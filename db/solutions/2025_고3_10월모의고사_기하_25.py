import numpy as np

# 원래 조건: 한 변=2 정사각형 BCDE, AB=AC=AD=AE, 직선 AC와 평면 BCDE 각도=π/3
B = np.array([-1, -1, 0])
C = np.array([ 1, -1, 0])
D = np.array([ 1,  1, 0])
E = np.array([-1,  1, 0])

# h^2=6에서 A 설정
h = np.sqrt(6)
A = np.array([0, 0, h])

# 검증 1: 정사각형 변 길이
assert abs(np.linalg.norm(C-B) - 2) < 1e-9, 'BC!=2'
assert abs(np.linalg.norm(D-C) - 2) < 1e-9, 'CD!=2'

# 검증 2: AB=AC=AD=AE
dists = [np.linalg.norm(A-X) for X in [B,C,D,E]]
assert max(dists)-min(dists) < 1e-9, 'AB!=AC!=AD!=AE'

# 검증 3: 직선 AC와 평면 BCDE의 각도=π/3
vAC = C - A
normal = np.array([0, 0, 1])
sin_theta = abs(np.dot(vAC, normal)) / np.linalg.norm(vAC)
angle = np.arcsin(sin_theta)
assert abs(angle - np.pi/3) < 1e-9, f'angle={angle} != pi/3'

# 검증 4: 삼각형 ABC 넓이 = sqrt(7)
AB = B - A
AC = C - A
cross = np.cross(AB, AC)
area = 0.5 * np.linalg.norm(cross)
expected = np.sqrt(7)
assert abs(area - expected) < 1e-9, f'area={area} != sqrt(7)={expected}'

print('VERIFY_PASS')
