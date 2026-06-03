import numpy as np
from sympy import *

# 주어진 조건: sin(-θ) = 1/3
# 따라서 sin(θ) = -1/3
sin_theta = -1/3
cos_theta = 2*sqrt(2)/3

# sin²θ + cos²θ = 1 검증
check1 = sin_theta**2 + float(cos_theta)**2
print(f'sin²θ + cos²θ = {check1}')
assert abs(check1 - 1.0) < 1e-10, 'VERIFY_FAIL'

# tan(θ) 계산
tan_theta_computed = sin_theta / float(cos_theta)
tan_theta_expected = float(-sqrt(2)/4)

print(f'tan(θ) computed = {tan_theta_computed}')
print(f'tan(θ) expected = {tan_theta_expected}')

assert abs(tan_theta_computed - tan_theta_expected) < 1e-10, 'VERIFY_FAIL'

# θ 범위 확인
theta_val = np.arcsin(-1/3)
if theta_val > 0:
    theta_val = 2*np.pi + theta_val
else:
    theta_val = 2*np.pi + theta_val

print(f'θ ≈ {theta_val:.6f}')
print(f'3π/2 ≈ {3*np.pi/2:.6f}')
print(f'2π ≈ {2*np.pi:.6f}')
assert 3*np.pi/2 < theta_val < 2*np.pi, 'VERIFY_FAIL'

print('VERIFY_PASS')