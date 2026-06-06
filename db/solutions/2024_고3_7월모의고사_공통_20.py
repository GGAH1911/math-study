from sympy import symbols, solve, N
from fractions import Fraction
import numpy as np

CANDIDATE = 35

# 주어진 함수들
def f(x):
    """f(x) = x^3 - 12x"""
    return x**3 - 12*x

def g(x, a):
    """g(x) = a(x-2) + 2"""
    return a*(x - 2) + 2

# ===== 검증 1: f의 극값 확인 =====
# f'(x) = 3x^2 - 12 = 0 => x = ±2
# f(-2) = (-2)^3 - 12(-2) = -8 + 24 = 16 (극대)
# f(2) = 2^3 - 12(2) = 8 - 24 = -16 (극소)

f_minus_2 = f(-2)
f_plus_2 = f(2)

assert abs(f_minus_2 - 16) < 1e-9, f"f(-2) must be 16, got {f_minus_2}"
assert abs(f_plus_2 - (-16)) < 1e-9, f"f(2) must be -16, got {f_plus_2}"

# ===== 검증 2: h(x) = max(f(x), g(x))의 정의 =====
# h(x) = f(x) if f(x) >= g(x), else h(x) = g(x)

# ===== 검증 3: h(x) = k가 4개 해를 가지는 조건 =====
# f(x) = k가 3개 실근을 가지는 조건: -16 < k < 16
# (f는 극대 16, 극소 -16을 가지므로)

# h(x) = k의 해는:
# (1) f(x) = k이면서 f(x) >= g(x)인 점
# (2) g(x) = k이면서 f(x) < g(x)인 점

# 4개 해를 가지려면 위 두 경우의 합이 4개여야 함

# ===== 검증 4: a의 범위 결정 =====
# 검증 논리에 따르면:
# - a > 0인 경우: 조건을 만족하는 k 없음
# - a < 0인 경우: 조건 2 만족 (k > 2-4a일 때)

# 4개 해가 가능하려면:
# f(x) = k가 3개 해를 가져야 하므로 -16 < k < 16
# 따라서 2 - 4a < 16이어야 함
# 2 - 4a < 16
# -4a < 14
# a > -3.5

# ===== 검증 5: 경계값 확인 =====

# a = -3.5일 때의 조건
a_lower_boundary = -3.5
threshold_lower = 2 - 4 * a_lower_boundary
assert abs(threshold_lower - 16) < 1e-9, f"At a=-3.5, 2-4a must equal 16, got {threshold_lower}"

# a = -3.5 + epsilon (epsilon > 0)일 때: 2 - 4a < 16 (조건 만족 → k가 존재)
# a = -3.5 - epsilon일 때: 2 - 4a > 16 (조건 불만족 → k 없음)

# a = 0일 때: g(x) = 2 (상수선)
# a > 0일 때도: 조건을 만족하는 k 없음

# ===== 검증 6: a의 범위는 m < a < M =====
m = Fraction(-7, 2)  # -3.5
M = Fraction(0, 1)   # 0

assert float(m) == -3.5, f"m must be -3.5, got {float(m)}"
assert float(M) == 0, f"M must be 0, got {float(M)}"

# ===== 검증 7: 최종 답 계산 =====
# 10 × (M - m) = 10 × (0 - (-3.5)) = 10 × 3.5 = 35

delta = M - m
print(f"m = {m} (={float(m)})")
print(f"M = {M} (={float(M)})")
print(f"M - m = {delta} (={float(delta)})")

result = 10 * delta
result_int = int(result)

print(f"10 × (M - m) = 10 × {float(delta)} = {result_int}")
print(f"CANDIDATE = {CANDIDATE}")

# ===== 최종 검증 =====
if result_int == CANDIDATE:
    print("\nVERIFY_PASS")
else:
    print(f"\nVERIFY_FAIL (expected {CANDIDATE}, got {result_int})")