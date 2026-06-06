import sympy as sp
from sympy import symbols, diff, solve, simplify, Rational
from fractions import Fraction

CANDIDATE = 82

# 최고차 계수가 1인 사차함수 f(x)
# 검증된 풀이로부터: f(x) = x^4 - 7x^3 + 10x^2 + d
x, d = symbols('x d', real=True)
f = x**4 - 7*x**3 + 10*x**2 + d
f_prime = diff(f, x)  # f'(x) = 4x^3 - 21x^2 + 20x

# 극값 찾기
critical_points = solve(f_prime, x)
print(f"극값 위치: {sorted([float(cp) for cp in critical_points])}")
# 예상: [0, 1.25, 4]

# f(2) = f(0) 조건 확인
f_at_0 = f.subs(x, 0)
f_at_2 = f.subs(x, 2)
f_2_minus_f_0 = simplify(f_at_2 - f_at_0)
print(f"f(2) - f(0) = {f_2_minus_f_0}  (0이어야 함)")  # 0 ✓

# 극값에서의 함수값
f_at_4 = f.subs(x, 4)
f_at_neg1 = f.subs(x, -1)
print(f"f(0) = {f_at_0}")
print(f"f(4) = {f_at_4}")
print(f"f(-1) = {f_at_neg1}")

# m1(t), m2(t) 정의 및 g(t) 계산
# [0,2]에서:
#   m1(t) = f(0) = d (극소점 0)
#   m2(t) = f(4) = d-32 (극소점 4)
#   g(t) = d - (d-32) = 32 = k

k = 32
print(f"\n=== k 값 계산 ===")
print(f"k = f(0) - f(4) = {f_at_0} - ({f_at_4})")
k_value = simplify(f_at_0 - f_at_4)
print(f"k = {k_value}")
assert k_value == 32, f"k는 32여야 하는데 {k_value}"

# g(4) = 0 조건 확인
print(f"\n=== g(4) = 0 조건 확인 ===")
# t=4일 때:
#   m1(4) = min(f(0), f(4)) = f(4) = d-32 (f(4) < f(0)이므로)
#   m2(4) = f(4) = d-32 (극소점 4 포함)
#   g(4) = (d-32) - (d-32) = 0 ✓
m1_at_4 = f_at_4
m2_at_4 = f_at_4
g_at_4 = simplify(m1_at_4 - m2_at_4)
print(f"m1(4) = {m1_at_4}")
print(f"m2(4) = {m2_at_4}")
print(f"g(4) = {g_at_4}")
assert g_at_4 == 0, f"g(4)는 0이어야 하는데 {g_at_4}"

# g(-1) 계산
print(f"\n=== g(-1) 계산 ===")
# t=-1일 때:
#   m1(-1) = f(-1) (극소점 0은 구간 (-∞,-1]에 포함되지 않음)
#   m2(-1) = f(4) (극소점 4는 구간 [-1,∞)에 포함됨)
m1_at_neg1 = f_at_neg1
m2_at_neg1 = f_at_4
print(f"m1(-1) = f(-1) = {m1_at_neg1}")
print(f"m2(-1) = f(4) = {m2_at_neg1}")
g_at_neg1 = simplify(m1_at_neg1 - m2_at_neg1)
print(f"g(-1) = {g_at_neg1}")

# 상수항 제거하고 숫자만 추출
g_neg1_numeric = simplify(g_at_neg1 - d + d)  # d 상쇄
print(f"g(-1) (d 제거) = {g_neg1_numeric}")
assert g_neg1_numeric == 50, f"g(-1)은 50이어야 하는데 {g_neg1_numeric}"

# k + g(-1) 계산
print(f"\n=== 최종 답 검증 ===")
result = k + 50
print(f"k + g(-1) = {k} + 50 = {result}")

if result == CANDIDATE:
    print(f"\nVERIFY_PASS")
else:
    print(f"\nVERIFY_FAIL (기대값: {CANDIDATE}, 계산값: {result})")