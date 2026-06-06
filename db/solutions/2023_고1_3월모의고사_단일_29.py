import sympy as sp
from sympy import Rational, sqrt, simplify

# 좌표 설정
b_y = Rational(-9, 2)

# E의 y좌표
y_E = -b_y / 4  # = 9/8

# 삼각형 EDG의 넓이
# E = (-b_x/4, 9/8), D = (0, 0), G = (1, 0)
# 밑변 DG = 1 (x축 위), 높이 = y_E
area_EDG = Rational(1, 2) * 1 * y_E
print(f'Area of EDG = {area_EDG}')

# p와 q 추출
numerator = area_EDG.p
denominator = area_EDG.q
print(f'p = {numerator}, q = {denominator}')
print(f'gcd(p, q) = {sp.gcd(numerator, denominator)}')
print(f'p + q = {numerator + denominator}')

if area_EDG == Rational(9, 16) and sp.gcd(9, 16) == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')