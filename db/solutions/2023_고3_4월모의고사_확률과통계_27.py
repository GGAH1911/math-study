from math import comb
import sympy as sp

x = sp.Symbol('x')
a = 2

# 원래 문제의 식: (ax - 2/(ax))^7
expr = (a*x - 2/(a*x))**7

# 전개식
expanded = sp.expand(expr)

# x^(-1)의 계수 추출
coeff_x_inv = expanded.as_coefficients_dict()[1/x]

print(f'x^(-1)의 계수: {coeff_x_inv}')

# 답이 280인지 확인
if coeff_x_inv == 280:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')