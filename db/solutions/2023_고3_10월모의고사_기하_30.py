import numpy as np
from scipy.spatial import distance

# 좌표 설정
A = np.array([-2, 0, 0])
B = np.array([2, 0, 0])
C = np.array([2, np.sqrt(15)/2, 3*np.sqrt(5)/2])
D = np.array([2, -np.sqrt(15)/2, 3*np.sqrt(5)/2])

# 구의 중심과 반지름
center = np.array([0, 0, np.sqrt(5)])
radius = 3

# 각 점이 구 위에 있는지 확인
dist_A = np.linalg.norm(A - center)
dist_B = np.linalg.norm(B - center)
dist_C = np.linalg.norm(C - center)
dist_D = np.linalg.norm(D - center)

print(f'dist_A: {dist_A:.10f}, radius: {radius}')
print(f'dist_B: {dist_B:.10f}, radius: {radius}')
print(f'dist_C: {dist_C:.10f}, radius: {radius}')
print(f'dist_D: {dist_D:.10f}, radius: {radius}')

# 조건 검증
bc = np.linalg.norm(C - B)
bd = np.linalg.norm(D - B)
print(f'BC: {bc:.10f}, should be {np.sqrt(15):.10f}')
print(f'BD: {bd:.10f}, should be {np.sqrt(15):.10f}')

# AB가 원 C의 지름인지 확인 (A, B가 z=0, x^2+y^2=4 위에 있는지)
print(f'A on circle C: x^2+y^2 = {(-2)**2 + 0**2}')
print(f'B on circle C: x^2+y^2 = {2**2 + 0**2}')

# 삼각형 ABC의 넓이
AB = B - A
AC = C - A
cross_ABC = np.cross(AB, AC)
area_ABC = 0.5 * np.linalg.norm(cross_ABC)
print(f'Area of ABC: {area_ABC:.10f}, should be {np.sqrt(15):.10f}')

# 정사영
AD = D - A
cross_ABD = np.cross(AB, AD)
cos_theta = np.abs(np.dot(cross_ABC, cross_ABD)) / (np.linalg.norm(cross_ABC) * np.linalg.norm(cross_ABD))
print(f'cos(theta): {cos_theta:.10f}, should be 0.5')

k = area_ABC * cos_theta
k_squared = k**2
print(f'k: {k:.10f}, should be {np.sqrt(15):.10f}')
print(f'k^2: {k_squared:.10f}')

if abs(k_squared - 15) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')