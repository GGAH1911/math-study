import numpy as np
from scipy.optimize import fsolve

# 좌표 설정
A = np.array([2, 4])
B = np.array([0, 0])
C = np.array([5, 0])
D = np.array([16/5, 12/5])

# 삼각형 ABC 검증
AB = np.linalg.norm(A - B)
AC = np.linalg.norm(A - C)
BC = np.linalg.norm(C - B)
assert abs(AB - 2*np.sqrt(5)) < 1e-10, f'AB={AB}, expected {2*np.sqrt(5)}'
assert abs(AC - 5) < 1e-10, f'AC={AC}'
assert abs(BC - 5) < 1e-10, f'BC={BC}'

# D가 원 위에 있는지 확인 (BC를 지름으로)
center = np.array([2.5, 0])
radius = 2.5
dist_D = np.linalg.norm(D - center)
assert abs(dist_D - radius) < 1e-10, f'D is not on circle: {dist_D} vs {radius}'

# sin(theta) = 44/125, cos(theta) = 117/125
sin_theta = 44/125
cos_theta = 117/125
theta = np.arcsin(sin_theta)

# E의 좌표
E = np.array([2.5 + 2.5*cos_theta, 2.5*sin_theta])

# CE 길이
CE = np.linalg.norm(E - C)
k = CE
expected_k = 2*np.sqrt(5)/5
assert abs(CE - expected_k) < 1e-10, f'CE={CE}, expected {expected_k}'

# 삼각형 DCE의 넓이
def triangle_area(p1, p2, p3):
    return 0.5 * abs((p2[0]-p1[0])*(p3[1]-p1[1]) - (p3[0]-p1[0])*(p2[1]-p1[1]))

area_DCE = triangle_area(D, C, E)
assert abs(area_DCE - 3/5) < 1e-10, f'Area={area_DCE}, expected {3/5}'

# CE < DE 확인
DE = np.linalg.norm(E - D)
assert CE < DE, f'CE={CE} should be < DE={DE}'

# 최종 답
result = 60 * k**2
assert abs(result - 48) < 1e-9, f'60k²={result}, expected 48'

print('VERIFY_PASS')