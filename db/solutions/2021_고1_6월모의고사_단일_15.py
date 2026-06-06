import numpy as np
from sympy import symbols, diff, solve

# 원래 식: b^2 = 4*a*(h-a), h=10
h = 10
a = symbols('a', real=True, positive=True)
b_squared = 4 * a * (h - a)

# 최댓값을 찾기 위해 미분
derivative = diff(b_squared, a)
critical_points = solve(derivative, a)
print(f'Critical points: {critical_points}')

# a=5에서의 b^2 값
a_max = 5
b_squared_max = 4 * a_max * (h - a_max)
print(f'b^2 at a=5: {b_squared_max}')

# 검증: 원래 식에 a=5, h=10 대입
verify_value = 4 * 5 * (10 - 5)
print(f'Verification: {verify_value}')

if verify_value == 100:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')