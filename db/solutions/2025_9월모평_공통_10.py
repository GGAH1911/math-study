import numpy as np
from math import sqrt, pi

# 좌표 설정
H = np.array([0, 0])
A = np.array([0, 2])
B = np.array([-6, 0])
C = np.array([4, 0])

# 조건 1: AB:AC = √2:1
AB = np.linalg.norm(A - B)
AC = np.linalg.norm(A - C)
ratio = AB / AC
print(f'AB={AB:.4f}, AC={AC:.4f}, AB/AC={ratio:.4f}, √2={sqrt(2):.4f}')
assert abs(ratio - sqrt(2)) < 1e-10, f'Ratio check failed'

# 조건 2: AH=2
AH = np.linalg.norm(A - H)
assert abs(AH - 2) < 1e-10, f'AH check failed'

# 조건 3: ∠A > π/2
vec_AB = B - A
vec_AC = C - A
dot_product = np.dot(vec_AB, vec_AC)
print(f'AB·AC={dot_product:.4f}')
assert dot_product < 0, f'Angle A must be > π/2'

# 조건 4: 외접원 반지름과 넓이
# 코사인 법칙으로 외접원 반지름 검증
BC = np.linalg.norm(C - B)
cos_A = dot_product / (AB * AC)
sin_A = sqrt(1 - cos_A**2)
R = BC / (2 * sin_A)
area_circle = pi * R**2
print(f'R={R:.4f}, 5√2={5*sqrt(2):.4f}')
print(f'Circle area={area_circle:.4f}, 50π={50*pi:.4f}')
assert abs(R - 5*sqrt(2)) < 1e-10, f'Circumradius check failed'
assert abs(area_circle - 50*pi) < 1e-10, f'Circle area check failed'

# 최종 답
BH = abs(B[0])
print(f'\nBH={BH}')
assert BH == 6, f'BH must be 6'
print('VERIFY_PASS')