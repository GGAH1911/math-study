import numpy as np
from math import sqrt

# 주어진 조건: 반지름 4, 높이 3
r = 4
h = 3

# 조건 (가)에서 sin²θ = 7/16, cos²θ = 9/16
sin_theta = sqrt(7) / 4
cos_theta = 3 / 4

# 좌표 설정
A = np.array([-4, 0, 0])
B = np.array([4, 0, 0])
C = np.array([4*cos_theta, 4*sin_theta, 3])
D = np.array([-4*cos_theta, 4*sin_theta, 3])  # φ = π - θ

# 검증 1: △ABC 넓이 = 16
AB = B - A
AC = C - A
cross = np.cross(AB, AC)
area_ABC = 0.5 * np.linalg.norm(cross)
print(f'△ABC 넓이: {area_ABC}')
if abs(area_ABC - 16) < 1e-10:
    print('조건 (가) 만족')
else:
    print('VERIFY_FAIL')
    exit()

# 검증 2: AB ∥ CD
CD = D - C
# AB 방향: (1, 0, 0), CD는 y=0, z=0에 평행해야 함
if abs(CD[1]) < 1e-10 and abs(CD[2]) < 1e-10:
    print('조건 (나) 만족: AB ∥ CD')
else:
    print('VERIFY_FAIL')
    exit()

# 답: |CD|
CD_length = np.linalg.norm(CD)
print(f'|CD| = {CD_length}')
if abs(CD_length - 6) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')