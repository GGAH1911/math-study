import math
from sympy import sqrt, simplify, gcd, Rational

# 쌍곡선의 초점
F = (3, 0)
Fp = (-3, 0)

# P, P' 좌표
P = (3, Rational(5,2))
Pp = (3, Rational(-5,2))

# Q 좌표
Q = (Rational(-93,169), Rational(345,338))

# 검증 1: QP' = 5
QPp_dist_sq = (Q[0] - Pp[0])**2 + (Q[1] - Pp[1])**2
QPp_dist = sqrt(QPp_dist_sq)
print(f'QP\' distance: {QPp_dist} (should be 5)')
assert simplify(QPp_dist - 5) == 0, 'QP\' should be 5'

# 검증 2: Q가 선분 F'P 위에 있는지
# Q = F' + t(P - F')
t = Rational(69,169)
Q_param = (Fp[0] + t*(P[0]-Fp[0]), Fp[1] + t*(P[1]-Fp[1]))
assert simplify(Q_param[0] - Q[0]) == 0 and simplify(Q_param[1] - Q[1]) == 0, 'Q not on F\'P'

# 검증 3: 타원의 장축 길이
QP_dist_sq = (Q[0] - P[0])**2 + (Q[1] - P[1])**2
QP_dist = sqrt(QP_dist_sq)
axis_length = QP_dist + QPp_dist
axis_simplified = simplify(axis_length)
print(f'Axis length (2a\'): {axis_simplified}')

# 기약분수로 정리
g = gcd(115, 13)
print(f'gcd(115, 13) = {g}')
print(f'p = 13, q = 115')
print(f'p + q = 128')

print('VERIFY_PASS')