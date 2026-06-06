import numpy as np
from math import sqrt, acos

# 구한 답: 넓이 = 12
a = 2*sqrt(5)
b = 4*sqrt(5)
c = 6
cos_C = 4/5
sin_C = 3/5

# 코사인 법칙으로 검증: c² = a² + b² - 2ab·cos(C)
c_squared_check = a**2 + b**2 - 2*a*b*cos_C
print(f'c² 검증: {c_squared_check} (예상: 36)')
print(f'일치: {abs(c_squared_check - 36) < 1e-10}')

# 정현법칙: a/sin(A) = b/sin(B) = c/sin(C)
ratio = c / sin_C
sin_A = a / ratio
sin_B = b / ratio
print(f'sin(A) = {sin_A}, sin(B) = {sin_B}')
print(f'2·sin(A) = {2*sin_A}, sin(B) = {sin_B}')
print(f'조건 2sin(A) = sin(B) 만족: {abs(2*sin_A - sin_B) < 1e-10}')

# 넓이 계산
area = 0.5 * a * b * sin_C
print(f'삼각형 넓이: {area}')
print(f'답이 정수: {abs(area - round(area)) < 1e-10}')
print(f'최종 답: {int(round(area))}')

if abs(area - 12) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')