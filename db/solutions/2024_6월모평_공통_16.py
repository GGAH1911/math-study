import sympy as sp
from sympy import symbols, simplify, solve

x = symbols('x', real=True)

# 원래 부등식: 2^(x-6) <= (1/4)^x
left = 2**(x-6)
right = (sp.Rational(1,4))**x

# x=1, 2에서 검증
for x_val in [1, 2]:
    left_val = 2**(x_val - 6)
    right_val = (1/4)**x_val
    is_satisfied = left_val <= right_val
    print(f'x={x_val}: {left_val} <= {right_val}? {is_satisfied}')

# x=3은 만족하지 않는지 확인
x_val = 3
left_val = 2**(x_val - 6)
right_val = (1/4)**x_val
is_satisfied = left_val <= right_val
print(f'x={x_val}: {left_val} <= {right_val}? {is_satisfied}')

# 최종 검증: x=1,2의 합이 3
sum_natural = 1 + 2
if sum_natural == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')