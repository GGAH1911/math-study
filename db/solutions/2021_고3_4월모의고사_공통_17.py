import math
from sympy import *

# 주어진 조건: sin(θ)cos(θ) = 7/18
# 구하는 값: 30(sin(θ) + cos(θ))

# sin(θ) + cos(θ) = t라고 놓으면
# t^2 = sin²(θ) + 2sin(θ)cos(θ) + cos²(θ) = 1 + 2sin(θ)cos(θ)
t_squared = 1 + 2 * Rational(7, 18)
print(f't² = {t_squared}')

# t = 4/3 (0 < θ < π/2 이므로 양수)
t = sqrt(t_squared)
print(f't = {t}')

# 최종 답
answer = 30 * t
print(f'30(sin θ + cos θ) = {answer}')

if answer == 40:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')