from sympy import sin, symbols, solve, Rational
import math

# 원에 내접한 삼각형: AC/sin(B) = 2R
# AC = 5, R = 4, angle B = theta
# 5/sin(theta) = 8
# sin(theta) = 5/8

sin_theta = Rational(5, 8)
print(f'sin(theta) = {sin_theta}')
print(f'sin(theta) decimal = {float(sin_theta)}')

# Check: is 5/8 a valid sine value (between 0 and 1)?
if 0 < sin_theta < 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')