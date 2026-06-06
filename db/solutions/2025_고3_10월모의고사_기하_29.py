import sympy as sp
from sympy import sqrt, symbols, simplify, solve

# 답 검증: a=4, b=8, c=4√5
a, b, c = 4, 8, 4*sqrt(5)

# P의 좌표
x0 = (a**2 + c**2)/(2*c)
y0 = b**3/(2*a*c)

# Q의 좌표
Q_y = b*c/a

# 조건 1: P가 쌍곡선 위의 점
hyperbola_check = x0**2/a**2 - y0**2/b**2 - 1
print(f'Hyperbola check: {simplify(hyperbola_check)}')

# 조건 2: |QF| = 20
Q_to_F = sqrt(c**2 + Q_y**2)
print(f'|QF| = {simplify(Q_to_F)}')

# 조건 3: 직선 PF의 기울기 = -b/a
slope_PF = y0 / (x0 - c)
print(f'Slope of PF: {simplify(slope_PF)} (expected: {-b/a})')

# 조건 4: ∠QPF' = π/2
PQ = (-x0, Q_y - y0)
PF_prime = (-c - x0, -y0)
dot_product = PQ[0] * PF_prime[0] + PQ[1] * PF_prime[1]
print(f'PQ·PF\' = {simplify(dot_product)}')

# 삼각형 OPQ의 넓이
area = abs(x0 * Q_y) / 2
print(f'Area of triangle OPQ: {simplify(area)}')

if simplify(hyperbola_check) == 0 and simplify(Q_to_F) == 20 and simplify(slope_PF) == -2 and simplify(dot_product) == 0:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')