import sympy as sp
from sympy import sqrt, symbols, solve, simplify

# 좌표 정의
A = (-1, sqrt(15))
B = (0, 0)
C = (6, 0)
M = (-sp.Rational(1, 2), sqrt(15)/2)
N = (sp.Rational(5, 2), sqrt(15)/2)
D = (-1, 0)

# MH 거리 계산
# 직선 DN: sqrt(15)*x - 7*y + sqrt(15) = 0
# 점 M에서 직선까지의 거리
a, b, c = sqrt(15), -7, sqrt(15)
dist = abs(a * M[0] + b * M[1] + c) / sqrt(a**2 + b**2)
dist_simplified = simplify(dist)

# 예상 답
expected = 3*sqrt(15)/8

# 검증
if simplify(dist_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {dist_simplified} != {expected}')