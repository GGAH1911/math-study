import math
from sympy import *

CANDIDATE = Rational(125, 2)

# 삼각형 ADC의 꼭짓점
A = (0, 0)
D = (12, 4)
C = (12, 9)

# 변의 길이
AD = sqrt((12-0)**2 + (4-0)**2)
DC = sqrt((12-12)**2 + (9-4)**2)
AC = sqrt((12-0)**2 + (9-0)**2)

print(f'AD = {AD} = {simplify(AD)}')
print(f'DC = {DC}')
print(f'AC = {AC}')

# 삼각형의 넓이 (외적 이용)
area = abs((D[0]-A[0])*(C[1]-A[1]) - (D[1]-A[1])*(C[0]-A[0])) / 2
print(f'Area = {area}')

# 외접원의 반지름
R_squared = (AD * DC * AC)**2 / (16 * area**2)
R = sqrt(R_squared)
print(f'R = {simplify(R)}')

# 외접원의 넓이
circumcircle_area = pi * R_squared
circumcircle_area_simplified = simplify(circumcircle_area)
print(f'외접원의 넓이 = {circumcircle_area_simplified}')

# 검증
if simplify(circumcircle_area_simplified - CANDIDATE * pi) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')