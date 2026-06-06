import sympy as sp
x, a = sp.symbols('x a', real=True)
# 부등식 |x-a|<5의 해는 a-5 < x < a+5
# a=1, b=6일 때
a_val = 1
b_val = 6
# |x-1|<5의 해는 -4 < x < 6
lower_bound = a_val - 5
upper_bound = a_val + 5
assert lower_bound == -4, f'Lower bound mismatch: {lower_bound} != -4'
assert upper_bound == b_val, f'Upper bound mismatch: {upper_bound} != {b_val}'
result = a_val + b_val
assert result == 7, f'Sum mismatch: {result} != 7'
print('VERIFY_PASS')