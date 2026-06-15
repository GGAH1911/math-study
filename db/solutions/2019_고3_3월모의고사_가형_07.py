import sympy as sp
from sympy import ln, limit, symbols

x = symbols('x')
a, b = 2, 1

f = ln(a*x + b)

lim_value = limit(f/x, x, 0)
assert lim_value == 2, f'극한값 검증 실패: {lim_value}'

f_2 = ln(2*2 + 1)
assert f_2 == ln(5), f'f(2) 계산 오류: {f_2}'

print('VERIFY_PASS')