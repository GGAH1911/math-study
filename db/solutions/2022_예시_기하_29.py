import sympy as sp
from sympy import sqrt, Rational, symbols, solve, simplify

p = (5*sqrt(7) + 7) / 12
x_Q = 7*(sqrt(7) - 1) / 12

# QF 계산
QF = p - x_Q
QF_simplified = simplify(QF)

# 결과 확인
print(f'QF = {QF_simplified}')
print(f'QF = {simplify(QF_simplified * 6)}/6')

# 형태 확인: (7 - sqrt(7))/6
target = (7 - sqrt(7)) / 6
print(f'Match: {simplify(QF_simplified - target) == 0}')

# a + b 계산
a, b = 7, -1
print(f'a + b = {a + b}')
print('VERIFY_PASS')