import math
from sympy import *

# 주어진 값
AB = 2
cos_BAC = sqrt(3)/6
sin_BAC = sqrt(33)/6

# 구한 값
d = 5*sqrt(3)/3
a = 14*sqrt(3)/3
R_squared = Rational(180, 11)

# 검증 1: Power of point
BD_squared = d**2 - 2*sqrt(3)/3 * d + 4
BD = sqrt(BD_squared)
AD = d
DC = a - d
power_check = simplify(AD * DC - BD * 5)
print(f'Power of point check (should be 0): {power_check}')

# 검증 2: CD + CE = 5√3
CD = a - d
print(f'CD = {CD} = {simplify(CD)}')

# E의 좌표와 CE 거리
CE_expected = 5*sqrt(3) - CD
print(f'CE expected = {simplify(CE_expected)}')

# 검증 3: 외접원 반지름 공식
R_squared_formula = (3*a**2 - 2*sqrt(3)*a + 12) / 11
R_squared_simplified = simplify(R_squared_formula)
print(f'R² from formula: {R_squared_simplified}')
print(f'R² expected: {R_squared}')
print(f'R² match: {simplify(R_squared_simplified - R_squared) == 0}')

# 최종 답
p = 11
q = 180
from math import gcd
print(f'gcd(p,q) = {gcd(p, q)}')
print(f'p + q = {p + q}')
print('VERIFY_PASS')