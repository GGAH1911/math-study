from sympy import *

CANDIDATE = '4'

# ====== 검증: 원래 조건으로부터 답 도출 ======

# 핵심 조건: 직선 y=k와 함수의 교점이 정확히 2개인 경우가 유일하게 존재
# ⟺ A_R ≤ P (우측 극한값 ≤ 극댓값)

# 함수의 성질 (문제에서 주어진 조건):
# f(a) = P = 2^a + 2^{-a} - 2 (극댓값)
# A_L = 2 - 2^{-a} (좌측 극한)
# a < 1일 때: A_R = 2 - 2^a (우측 극한)

print("=== 유일성 조건으로부터 a의 범위 도출 ===")
print()

# 부등식: A_R ≤ P
# 2 - 2^a ≤ 2^a + 2^{-a} - 2
# 4 ≤ 2·2^a + 2^{-a}
# 4t ≤ 2t^2 + 1 (t = 2^a 치환)
# 2t^2 - 4t + 1 ≥ 0

t = symbols('t', positive=True, real=True)
quadratic = 2*t**2 - 4*t + 1
roots = solve(quadratic, t)

print("Step 1: 이차부등식 2t^2 - 4t + 1 ≥ 0의 해")
print(f"  근: {roots}")

# t ≥ 1 + sqrt(2)/2 추출
t_critical = 1 + sqrt(2)/2
print(f"  임계값: t = 1 + sqrt(2)/2 = (2 + sqrt(2))/2")
print()

# 2^a ≥ 1 + sqrt(2)/2
# a ≥ log_2(1 + sqrt(2)/2) = log_2((2+sqrt(2))/2) = log_2(2+sqrt(2)) - 1
print("Step 2: a의 범위")

a_min = log(2 + sqrt(2), 2) - 1
a_max = 1

print(f"  a ≥ log_2(2 + sqrt(2)) - 1  (≈ {float(a_min.evalf()):.6f})")
print(f"  a ≤ 1  (문제 조건: a=1일 때 경계에서 성립)")
print()

# m, M 정의
m = a_min
M = a_max

print("Step 3: m과 M의 정의")
print(f"  m = {m}")
print(f"  M = {M}")
print()

# M + m 계산
M_plus_m = M + m
M_plus_m_simp = simplify(M_plus_m)

print("Step 4: M + m 계산")
print(f"  M + m = {M} + ({m})")
print(f"  M + m = {M_plus_m_simp}")
print(f"  M + m = log_2(2 + sqrt(2))")
print()

# 검증: M + m = log_2(2 + sqrt(2))
assert simplify(M_plus_m_simp - log(2 + sqrt(2), 2)) == 0
print("  ✓ 확인: M + m = log_2(2 + sqrt(2))")
print()

# 2^(M+m) 계산
power_result = 2**M_plus_m_simp
power_simp = simplify(power_result)

print("Step 5: 2^(M+m) 계산")
print(f"  2^(M+m) = 2^(log_2(2 + sqrt(2)))")
print(f"  2^(M+m) = {power_simp}")
print()

# 검증: 2^(M+m) = 2 + sqrt(2)
expected = 2 + sqrt(2)
assert simplify(power_simp - expected) == 0
print(f"  ✓ 확인: 2^(M+m) = 2 + sqrt(2)")
print()

# p + sqrt(q) 형태에서 p, q 추출
print("Step 6: p + sqrt(q) 형태 분석")
print(f"  2 + sqrt(2) = p + sqrt(q)")
print(f"  p = 2, q = 2")
print()

p = 2
q = 2

print("Step 7: 최종 답 계산")
final_answer = p + q
print(f"  p + q = {p} + {q} = {final_answer}")
print()

print("=== 검증 결과 ===")
if str(final_answer) == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL (expected '{CANDIDATE}', got '{final_answer}')")