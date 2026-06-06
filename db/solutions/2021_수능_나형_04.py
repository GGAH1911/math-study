import numpy as np
from sympy import symbols, cos, diff, solve, simplify

# 원함수
x = symbols('x', real=True)
f = 4*cos(x) + 3

# cos(x)의 범위는 [-1, 1]
# 최댓값은 cos(x) = 1일 때
max_value = f.subs(cos(x), 1)
print(f'Maximum value: {max_value}')

if max_value == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')