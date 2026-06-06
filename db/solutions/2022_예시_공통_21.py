import sympy as sp
from sympy import sqrt, cos, sin, pi, simplify

# 구한 각도의 삼각함수 값
sin_alpha = 4*sqrt(34)/51
cos_alpha = 11*sqrt(17)/51
sin_beta = 2*sqrt(34)/17
cos_beta = 3*sqrt(17)/17

# 조건 검증 1: sin(beta)/sin(alpha) = 3/2
ratio = simplify(sin_beta / sin_alpha)
assert ratio == sp.Rational(3, 2), f'ratio check failed: {ratio}'

# 조건 검증 2: cos(alpha+beta) = 1/3
cos_sum = simplify(cos_alpha*cos_beta - sin_alpha*sin_beta)
assert cos_sum == sp.Rational(1, 3), f'cos_sum check failed: {cos_sum}'

# R과 R' 계산
R_prime = 2*sqrt(17)/17
R = 3*sqrt(17)/17

# 조건 검증 3: |OO'| = 1
OO_dist = simplify(R*cos_alpha + R_prime*cos_beta)
assert OO_dist == 1, f'OO distance check failed: {OO_dist}'

# 외접원 넓이 = pi*R^2
area_coeff = simplify(R**2)
assert area_coeff == sp.Rational(9, 17), f'area coefficient check failed: {area_coeff}'

print('VERIFY_PASS')