import math
from sympy import sqrt, simplify

# 벡터의 내적과 크기
v_l = (3, -1)
v_m = (7, 1)

# 내적
dot_product = v_l[0]*v_m[0] + v_l[1]*v_m[1]
print(f'dot product: {dot_product}')

# 크기
mag_l = math.sqrt(v_l[0]**2 + v_l[1]**2)
mag_m = math.sqrt(v_m[0]**2 + v_m[1]**2)
print(f'|v_l| = {mag_l}, |v_m| = {mag_m}')

# 코사인
cos_theta = abs(dot_product) / (mag_l * mag_m)
print(f'cos(theta) = {cos_theta}')

# 정답과 비교
expected = 2*math.sqrt(5)/5
print(f'expected: {expected}')
print(f'match: {abs(cos_theta - expected) < 1e-10}')

if abs(cos_theta - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')