import sympy as sp
from sympy import sqrt, Rational

# a의 값
a = sqrt(2) / 32
a_one_third = sqrt(2) / 4
a_two_thirds = Rational(1, 8)

# P와 Q의 좌표
P = (Rational(1, 4), sqrt(2))
Q = (-Rational(1, 8), sqrt(2) / 4)

# P가 y^2 = 8x를 만족하는지 확인
assert P[1]**2 == 8 * P[0], f'P not on C1'

# P가 x^2 = ay를 만족하는지 확인
assert P[0]**2 == a * P[1], f'P not on parabola'

# Q가 y^2 = -x를 만족하는지 확인
assert Q[1]**2 == -Q[0], f'Q not on C2'

# Q가 x^2 = ay를 만족하는지 확인
assert Q[0]**2 == a * Q[1], f'Q not on parabola'

# PQ의 기울기 확인
slope = (P[1] - Q[1]) / (P[0] - Q[0])
assert slope == 2*sqrt(2), f'Slope mismatch: {slope}'

# F1P와 F2Q 계산
F1P = P[0] + 2
F2Q = Rational(1, 4) - Q[0]

result = F1P + F2Q
assert result == Rational(21, 8), f'Result mismatch: {result}'

print('VERIFY_PASS')