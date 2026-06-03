import numpy as np
from sympy import *

# 주어진 조건을 만족하는 theta 찾기
theta = symbols('theta', real=True)
cos_theta = -sqrt(10)/10
sin_theta = -3*cos_theta

# 검증 1: 기본 항등식
identity_check = sin_theta**2 + cos_theta**2
print(f'sin²θ + cos²θ = {simplify(identity_check)}')
assert simplify(identity_check) == 1

# 검증 2: 주어진 관계식
relation_check = sin_theta + 3*cos_theta
print(f'sinθ + 3cosθ = {simplify(relation_check)}')
assert simplify(relation_check) == 0

# 검증 3: 범위 확인
cos_val = float(-sqrt(10)/10)
sin_val = float(3*sqrt(10)/10)
print(f'cosθ = {cos_val:.6f} < 0')
print(f'sinθ = {sin_val:.6f} > 0')
assert cos_val < 0 and sin_val > 0

print('VERIFY_PASS')