import numpy as np
from sympy import symbols, limit, oo

# 함수 정의
def f_right_of_0(x):
    """x in (0, 1): f(x) = 1 - 2x"""
    return 1 - 2*x

def f_right_of_1(x):
    """x in [1, 2]: f(x) = 2x - 3"""
    return 2*x - 3

# 극한값 계산
x = symbols('x')
lim_0_plus = limit(f_right_of_0(x), x, 0, '+')
lim_2_minus = limit(f_right_of_1(x), x, 2, '-')

result = lim_0_plus + lim_2_minus

print(f'lim(x→0+) f(x) = {lim_0_plus}')
print(f'lim(x→2-) f(x) = {lim_2_minus}')
print(f'Sum = {result}')

if result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')