import sympy as sp
from sympy import sqrt, Rational

b_sq = Rational(1, 2)
b = sqrt(b_sq)

# 점들의 좌표
P = (2 * b_sq, 4 * b)
F_prime = (-2, 4 * b)
Q_x = (2 * b_sq**3) / (2 + b_sq)**2
Q_y = (-4 * b**3) / (2 + b_sq)
Q = (Q_x, Q_y)
F = (2, 0)

# 거리 계산
def distance(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

dist_PF_prime = distance(P, F_prime)
dist_F_prime_Q = distance(F_prime, Q)
dist_Q_F = distance(Q, F)
dist_F_P = distance(F, P)

# 둘레
perimeter = dist_PF_prime + dist_F_prime_Q + dist_Q_F + dist_F_P
perimeter_simplified = sp.simplify(perimeter)

# 삼각형 PF'Q의 넓이
# P와 F'의 y좌표가 같으므로
base = abs(P[0] - F_prime[0])
height = abs(P[1] - Q[1])
area = Rational(1, 2) * base * height
area_simplified = sp.simplify(area)

print(f"P = {P}")
print(f"F' = {F_prime}")
print(f"Q = ({sp.simplify(Q[0])}, {sp.simplify(Q[1])})")
print(f"F = {F}")
print(f"\n둘레 = {perimeter_simplified}")
print(f"넓이 = {area_simplified}")
print(f"\n넓이 = {sp.simplify(area_simplified / sqrt(2))}√2")

# 넓이가 q/p * sqrt(2) 형태인지 확인
if sp.simplify(area_simplified - Rational(18, 5) * sqrt(2)) == 0:
    print("\nVERIFY_PASS")
else:
    print("\nVERIFY_FAIL")