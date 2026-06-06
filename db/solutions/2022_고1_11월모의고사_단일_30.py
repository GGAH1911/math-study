CANDIDATE = 48

from sympy import sqrt, simplify, Rational, solve, symbols

# ============= 문제 조건 재구성 =============

# 주어진 함수: f(x) = ax^2, g(x) = mx + 4a
# f, g의 교점을 A, B라 할 때, 세 조건:
# (1) 탈레스 정리: 원 C가 O, A, B를 지나고 AB를 지름 → OA·OB=0
# (2) 원 C가 f(x)와 네 점에서 만남 → 추가 교점 P 존재
# (3) 넓이 비율: S(ABP)/S(AOB) = 5

# ============= 단계 1: 탈레스 정리에서 a 도출 =============
# 교점: ax^2 = mx + 4a → ax^2 - mx - 4a = 0
# 비에타: x1·x2 = -4a/a = -4
# OA·OB = x1·x2 + (ax1^2)·(ax2^2) = x1·x2(1 + a^2·x1·x2) = 0
# -4(1 - 4a^2) = 0 → a^2 = 1/4 → a = 1/2

a = Rational(1, 2)
print(f"검증: a = {a}")

# ============= 단계 2: 넓이 조건에서 m 도출 =============
# 교점 방정식: (1/2)x^2 = mx + 2 → x^2 - 2mx - 4 = 0
# 비에타: x1 + x2 = 2m, x1·x2 = -4
# 직선 AB: y = mx + 2 (또는 mx - y + 2 = 0)

# 원의 방정식에 y = x^2/2 대입하면 4차식:
# x(x^3/4 - (1+m^2)x - 2m) = 0
# 근: 0, x1, x2, k
# 비에타(3차 부분): x1 + x2 + k = 0 → k = -2m

# P = (k, f(k)) = (-2m, 2m^2)
# 직선 AB로부터의 거리비: d(P,AB)/d(O,AB) = |−4m^2+2|/2 = 5
# |2 - 4m^2| = 10
# m^2 = 3 (m^2 = -2는 불가능) → m = sqrt(3)

m = sqrt(3)
print(f"검증: m = {m}")

# ============= 단계 3: 교점 검증 =============
x = symbols('x')
eq_intersection = a * x**2 - (m * x + 4*a)
roots_intersection = solve(eq_intersection, x)
x1, x2 = sorted(roots_intersection, key=lambda t: float(t.evalf()))

sum_check = simplify(x1 + x2)
prod_check = simplify(x1 * x2)
print(f"\n교점 비에타 검증:")
print(f"  x1 + x2 = {sum_check}, 예상: 2m = {2*m}")
print(f"  x1·x2 = {prod_check}, 예상: -4")

assert sum_check == 2*m, "교점 합이 맞지 않음"
assert prod_check == -4, "교점 곱이 맞지 않음"

# ============= 단계 4: k와 P의 좌표 =============
k = -2 * m
P_y = a * k**2

print(f"\nP의 좌표:")
print(f"  k = {k}")
print(f"  P = ({k}, {simplify(P_y)})")

# ============= 단계 5: 최종 계산 =============
def f(x_val):
    return a * x_val**2

def g(x_val):
    return m * x_val + 4*a

f_k = f(k)
g_minus_k = g(-k)

f_k_simp = simplify(f_k)
g_minus_k_simp = simplify(g_minus_k)

print(f"\n최종 계산:")
print(f"  f(k) = f({k}) = {f_k_simp}")
print(f"  g(-k) = g({-k}) = {g_minus_k_simp}")

answer = simplify(f_k * g_minus_k)
print(f"  f(k) × g(-k) = {answer}")

# ============= 결과 검증 =============
if answer == CANDIDATE:
    print(f"\nVERIFY_PASS")
else:
    print(f"\nVERIFY_FAIL (expected {CANDIDATE}, got {answer})")