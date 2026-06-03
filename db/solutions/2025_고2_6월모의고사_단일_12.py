import math
from sympy import *

# 주어진 조건
R = sqrt(7)
AB = 3*sqrt(3)
BC = 2*sqrt(3)
angle_ABC = pi/3

# AC 계산 (코사인 법칙)
AC_squared = AB**2 + BC**2 - 2*AB*BC*cos(angle_ABC)
AC = sqrt(AC_squared)
print(f'AC = {AC}')
print(f'AC simplified = {simplify(AC)}')

# 외접원의 반지름 검증 (정현법칙)
R_check = AC / (2*sin(angle_ABC))
print(f'R from sine rule = {R_check}')
print(f'R from sine rule simplified = {simplify(R_check)}')
print(f'R expected = {R}')

# 외접원의 넓이 검증
area_circle = pi * R**2
print(f'Circle area = {area_circle}')

# 삼각형의 넓이
triangle_area = Rational(1, 2) * AB * BC * sin(angle_ABC)
print(f'Triangle area = {triangle_area}')
print(f'Triangle area simplified = {simplify(triangle_area)}')

# 최종 검증
expected_answer = Rational(9, 2) * sqrt(3)
if simplify(triangle_area - expected_answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')