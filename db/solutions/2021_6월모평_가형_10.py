import sympy as sp
import numpy as np
from sympy import cos, exp, pi, symbols, limit, oo, simplify

x = symbols('x', real=True)
a_val = 4

# 원래 주어진 함수 방정식
# (e^(2x) - 1)^2 * f(x) = a - 4*cos(pi*x/2)
# f(0)은 연속성 조건에서 극한으로 정의됨

f_expr = (a_val - 4*cos(pi*x/2)) / (exp(2*x) - 1)**2
f_0 = limit(f_expr, x, 0)

print(f'f(0) = {f_0}')
print(f'f(0) simplified = {simplify(f_0)}')

result = a_val * f_0
print(f'a * f(0) = {result}')
print(f'a * f(0) simplified = {simplify(result)}')

# 검증: 극한이 맞는지 확인
if simplify(result - pi**2/2) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')