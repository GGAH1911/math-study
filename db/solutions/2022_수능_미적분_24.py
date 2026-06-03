import sympy as sp
import numpy as np
from sympy import exp, symbols, diff, solve

x = symbols('x', real=True)

# 원래 함수방정식: f(x^3 + x) = e^x
# 양변을 x에 대해 미분하면: f'(x^3 + x) * (3x^2 + 1) = e^x
# 따라서 f'(x^3 + x) = e^x / (3x^2 + 1)

# f'(2)를 구하려면 x^3 + x = 2인 x를 찾아야 함
eq = x**3 + x - 2
solution = solve(eq, x)
print(f'x^3 + x = 2의 해: {solution}')

# x = 1이 해임을 확인
x_val = 1
if x_val**3 + x_val == 2:
    # f'(2) = e^1 / (3*1^2 + 1) = e / 4
    f_prime_2 = exp(1) / (3*1**2 + 1)
    print(f'f\'(2) = {f_prime_2}')
    
    expected = exp(1) / 4
    if sp.simplify(f_prime_2 - expected) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')