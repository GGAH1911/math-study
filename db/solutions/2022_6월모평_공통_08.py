import numpy as np
from sympy import symbols, solve, simplify, expand

a = symbols('a')
x = symbols('x')

# f(x)^2이 x=a에서 연속 조건
# 좌극한: (-2a+6)^2
# 우극한: a^2

left_limit_squared = (-2*a + 6)**2
right_limit_squared = a**2

# 연속 조건
continuity_eq = left_limit_squared - right_limit_squared
continuity_eq_simplified = expand(continuity_eq)

# a의 값 구하기
a_values = solve(continuity_eq_simplified, a)
print(f'연속 조건 식: {continuity_eq_simplified} = 0')
print(f'해: a = {a_values}')

# 검증
sum_a = sum(a_values)
print(f'\n모든 a의 합: {sum_a}')

# 각 a값에 대해 검증
for a_val in a_values:
    left = (-2*a_val + 6)**2
    right = a_val**2
    print(f'\na = {a_val}:')
    print(f'  좌극한 (f(x))^2 = {left}')
    print(f'  우극한·함숫값 (f(a))^2 = {right}')
    print(f'  연속? {left == right}')

if sum_a == 8:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')