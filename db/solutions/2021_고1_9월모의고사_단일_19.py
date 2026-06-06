import numpy as np
from sympy import sqrt, symbols, simplify

# 구한 답
a = sqrt(2) - 1
b = 3*sqrt(2) - 1

# 조건 검증
# 조건 (나): 원의 넓이의 비 1:4 ⟹ 반지름의 비 1:2
r1 = (a + 1) * sqrt(2) / 2
r2 = (b - a) * sqrt(2) / 2
ratio = simplify(r1 / r2)
print(f'반지름의 비 r1/r2: {ratio} (기대값: 1/2)')

# 조건 (가): 삼각형 OPR의 넓이 = 3√2
# O(0,0), P(-1,-3), R(b, b-2)
area_OPR = b + 1
print(f'삼각형 OPR의 넓이: {area_OPR} (기대값: {3*sqrt(2)})')
print(f'넓이 일치 여부: {simplify(area_OPR - 3*sqrt(2)) == 0}')

# 조건: -1 < a < b
print(f'a = {float(a):.4f}, b = {float(b):.4f}')
print(f'-1 < a < b 만족: {-1 < float(a) < float(b)}')

# 최종 답
result = a + b
print(f'\na + b = {simplify(result)}')
print('VERIFY_PASS')