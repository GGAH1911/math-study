import sympy as sp
from sympy import sqrt, Rational

# 주어진 조건 검증
a = Rational(5, 2) * sqrt(2)
r = 3
m = Rational(1, 7)

# 직선 y = mx에서 중심 A까지의 거리
# 직선: mx - y = 0
# 거리 = |m*a - a| / sqrt(m^2 + 1)
dist = abs(m * a - a) / sqrt(m**2 + 1)
print(f"원의 중심에서 직선까지의 거리: {dist}")
print(f"반지름: {r}")
print(f"거리 == 반지름? {sp.simplify(dist - r) == 0}")

# 접선 조건 검증
a_sq = a**2
term1 = (a_sq - r**2) * (m**2 + 1)
term2 = 2 * a_sq * m
print(f"\n접선 조건 검증:")
print(f"(a^2 - r^2)(m^2 + 1) = {sp.simplify(term1)}")
print(f"2*a^2*m = {sp.simplify(term2)}")
print(f"조건 만족? {sp.simplify(term1 - term2) == 0}")

if sp.simplify(dist - r) == 0 and sp.simplify(term1 - term2) == 0:
    print("\nVERIFY_PASS")
else:
    print("\nVERIFY_FAIL")