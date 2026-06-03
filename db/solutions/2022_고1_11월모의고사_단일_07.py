import numpy as np
from sympy import symbols, solve, Poly

x = symbols('x', real=True)

# 첫 번째 부등식: 2x - 6 >= 0
cond1 = 2*x - 6 >= 0

# 두 번째 부등식: x^2 - 8x + 12 <= 0
cond2 = x**2 - 8*x + 12 <= 0

# 연립부등식 해
sol_cond2 = solve(x**2 - 8*x + 12 <= 0)
print(f'2x - 6 >= 0 => x >= 3')
print(f'x^2 - 8x + 12 <= 0 => (x-2)(x-6) <= 0 => 2 <= x <= 6')
print(f'Intersection: 3 <= x <= 6')

# 자연수 확인
natural_nums = [3, 4, 5, 6]
total = 0
for num in natural_nums:
    cond1_check = 2*num - 6 >= 0
    cond2_check = num**2 - 8*num + 12 <= 0
    if cond1_check and cond2_check:
        total += num

if total == 18:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')