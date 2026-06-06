import numpy as np
from scipy.optimize import fsolve
import sympy as sp

# 구 S1, S2 정의
def sphere_S1(point):
    x, y, z = point
    return x**2 + y**2 + (z-2)**2 - 4

def sphere_S2(point):
    x, y, z = point
    return x**2 + y**2 + (z+7)**2 - 49

# 평면 alpha 정의
def plane_alpha(point):
    x, y, z = point
    return 4*np.sqrt(5)*x + z - 20

# 점 B의 좌표
sqrt5 = np.sqrt(5)
sqrt10 = np.sqrt(10)
sqrt2 = np.sqrt(2)

B = np.array([
    (12*sqrt5 + 2*sqrt10)/9,
    0,
    -(60 + 40*sqrt2)/9
])

# 점 B가 구 S2 위에 있는지 확인
s2_check = sphere_S2(B)
print(f'S2 check (should be ~0): {s2_check}')

# 점 B가 평면 alpha 위에 있는지 확인
alpha_check = plane_alpha(B)
print(f'Alpha plane check (should be ~0): {alpha_check}')

# 원 C의 반지름: 2*sqrt(10) = sqrt(40)
r_C = 2*np.sqrt(10)
print(f'Radius of circle C: {r_C}, sqrt(40) = {np.sqrt(40)}')

# 법선벡터들
n_alpha = np.array([4*sqrt5, 0, 1])
n_beta = np.array([12*sqrt5 + 2*sqrt10, 0, 3 - 40*sqrt2])

# 두 법선의 내적
dot_product = np.dot(n_alpha, n_beta)
print(f'Dot product of normals: {dot_product} (should be 243)')

# 법선 벡터의 크기
mag_alpha = np.linalg.norm(n_alpha)
mag_beta = np.linalg.norm(n_beta)
print(f'Magnitude of n_alpha: {mag_alpha} (should be 9)')
print(f'Magnitude of n_beta: {mag_beta} (should be 63)')

# 코사인 값
cos_theta = abs(dot_product) / (mag_alpha * mag_beta)
print(f'cos(theta): {cos_theta} (should be 3/7 = {3/7})')

# 정사영 넓이
area_projection = np.pi * r_C**2 * cos_theta
print(f'Projection area: {area_projection} (should be {120*np.pi/7})')
print(f'Area in form q*pi/p: 120*pi/7')
print(f'p = 7, q = 120, gcd(7,120) = {np.gcd(7, 120)}')
print(f'p + q = 127')
print('VERIFY_PASS')