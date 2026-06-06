import numpy as np
from scipy.optimize import fsolve

# 주어진 점
P = np.array([-5., 6.])
R = np.array([3., 10.])
B = np.array([-8., 0.])

# 조건 확인: |3*XP + XR| = |PR|
vec_PR = R - P
dist_PR = np.linalg.norm(vec_PR)
print(f'|PR| = {dist_PR}')
print(f'|PR|^2 = {dist_PR**2}')

# 중심이 (-3, 7)이고 반지름이 sqrt(5)인 원
center = np.array([-3., 7.])
radius = np.sqrt(5)

# B에서 중심까지의 거리
dist_B_to_center = np.linalg.norm(B - center)
print(f'd(B, center) = {dist_B_to_center}')
print(f'd(B, center)^2 = {dist_B_to_center**2}')

# 최댓값과 최솟값
M = dist_B_to_center + radius
m = dist_B_to_center - radius

print(f'M = {M}')
print(f'm = {m}')
print(f'M * m = {M * m}')

# 검증: M*m = (sqrt(74))^2 - (sqrt(5))^2 = 74 - 5 = 69
product = dist_B_to_center**2 - radius**2
print(f'M*m (검증) = {product}')

if abs(product - 69) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')