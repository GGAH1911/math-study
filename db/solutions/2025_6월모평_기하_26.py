import sympy as sp
import numpy as np
from sympy import sqrt, symbols, simplify

a, b, c = 4, 4, 4*sqrt(2)

# 쌍곡선 방정식 검증: x = c일 때
x_val = c
y_sym = symbols('y')
hyperbola_eq = x_val**2 / a**2 - y_sym**2 / b**2 - 1
y_solutions = sp.solve(hyperbola_eq, y_sym)
print(f'y = {y_solutions}')

# PQ 거리 계산
PQ_dist = abs(y_solutions[0] - y_solutions[1])
print(f'PQ = {PQ_dist}')
assert PQ_dist == 8, f'PQ should be 8, got {PQ_dist}'

# 점근선 검증
asymptote_slope = b / a
print(f'Asymptote slope = {asymptote_slope}')
assert asymptote_slope == 1, 'Asymptote slope should be 1'

# 초점 검증
c_check = sqrt(a**2 + b**2)
print(f'c = {c_check}')
assert simplify(c_check - c) == 0, 'c value incorrect'

# 최종 답
answer = a**2 + b**2 + c**2
print(f'a² + b² + c² = {answer}')
assert answer == 64, f'Answer should be 64, got {answer}'

print('VERIFY_PASS')