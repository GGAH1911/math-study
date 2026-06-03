import math
from sympy import *

# 원에 내접하는 삼각형의 정현법칙
# a / sin(A) = 2R
# BC / sin(A) = 2R

R = 6
sin_A = Rational(1, 4)

# 정현법칙에서 BC 계산
BC = 2 * R * sin_A

# BC = 3인지 확인
print(f'BC = {BC}')
print(f'BC (float) = {float(BC)}')

# 검증: BC/sin(A) = 2R인지 확인
result = BC / sin_A
expected = 2 * R
print(f'BC / sin(A) = {result}')
print(f'2R = {expected}')

if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')