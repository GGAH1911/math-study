import math
from math import sqrt

# 방향벡터
u1 = (2, 1)
u2 = (1, 3)

# 내적
dot_product = u1[0] * u2[0] + u1[1] * u2[1]
print(f'내적: {dot_product}')

# 크기
mag_u1 = sqrt(u1[0]**2 + u1[1]**2)
mag_u2 = sqrt(u2[0]**2 + u2[1]**2)
print(f'|u1|: {mag_u1}, |u2|: {mag_u2}')

# 코사인 값
cos_theta = abs(dot_product) / (mag_u1 * mag_u2)
print(f'cos(θ): {cos_theta}')

# 답 검증
answer_value = sqrt(2) / 2
print(f'√2/2: {answer_value}')

if abs(cos_theta - answer_value) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')