import math
from sympy import *

# 주어진 조건: tan(theta) = 1/3
# cos^2(theta) = 9/10을 검증

cos_squared = Rational(9, 10)
sin_squared = 1 - cos_squared  # = 1/10

# tan^2(theta) = sin^2(theta)/cos^2(theta)
tan_squared = sin_squared / cos_squared
tan_theta = sqrt(tan_squared)

print(f'cos²θ = {cos_squared}')
print(f'sin²θ = {sin_squared}')
print(f'tan θ = {tan_theta}')
print(f'Expected tan θ = 1/3: {tan_theta == Rational(1,3)}')

# 최종 답 검증
result = 50 * cos_squared
print(f'50·cos²θ = {result}')

if result == 45:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')