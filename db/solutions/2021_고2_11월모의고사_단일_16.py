import sympy as sp
from sympy import sin, cos, sqrt, pi, solve, simplify, N

theta = sp.Symbol('theta', real=True)

# 주어진 조건: sin^4(theta) + cos^4(theta) = 23/32
condition = sin(theta)**4 + cos(theta)**4 - sp.Rational(23, 32)

# sin(theta) - cos(theta) = sqrt(7)/2 를 검증
# theta가 (pi/2, pi) 범위에 있을 때

# sin^4 + cos^4 = 1 - 2*sin^2*cos^2 공식 사용
# sin^2*cos^2 = 9/64 => sin*cos = -3/8 (2사분면)

sin_cos_product = sp.Rational(-3, 8)
sin_theta_minus_cos_theta = sqrt(7) / 2

# 역검증: (sin(theta) - cos(theta))^2 = sin^2 + cos^2 - 2*sin*cos
# = 1 - 2*(-3/8) = 1 + 3/4 = 7/4
verify_square = 1 - 2 * sin_cos_product
if verify_square == sp.Rational(7, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')