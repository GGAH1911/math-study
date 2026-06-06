from sympy import symbols, solve, Poly

CANDIDATE = 208

# 문제에서 도출된 삼차함수 (최고차항의 계수가 1)
def f(x):
    return x**3 - 6*x**2 + 9*x - 2

def f_prime(x):
    return 3*x**2 - 12*x + 9

# ===== 원래 문제 조건으로 검증 =====

# 검증 1: 극값점 확인
# f'(x) = 3(x-1)(x-3) = 0에서 x = 1, 3
x_sym = symbols('x')
critical_roots = solve(f_prime(x_sym), x_sym)
assert critical_roots == [1, 3], f"극값점: {critical_roots} (1, 3 필요)"

# 검증 2: 극값 확인 (a_4 = 1에서 극대, a_8 = 3에서 극소)
f_1 = f(1)
f_3 = f(3)
assert f_1 == 2, f"f(1) = {f_1}, 2 필요"
assert f_3 == -2, f"f(3) = {f_3}, -2 필요"

# 검증 3: f(0) 계산
f_0 = f(0)
assert f_0 == -2, f"f(0) = {f_0}, -2 필요"

# 검증 4: 조건 (나) - f(a_m) = f(0)
# f(3) = f(0) = -2이므로 a_8 = 3에서 조건 만족
# 따라서 m = 8
m = 8
assert f(3) == f_0, "f(a_8) = f(0) 만족하지 않음"

# 검증 5: f(m) 계산
f_m = f(m)
expected_f_m = m**3 - 6*m**2 + 9*m - 2
assert f_m == 198, f"f({m}) = {f_m}, 198 필요"
assert f_m == expected_f_m, f"계산 불일치: {f_m} vs {expected_f_m}"

# 검증 6: (3, ∞)에서 f(a_k) = k - 10 (k ≥ 9)
# CANDIDATE = 208일 때 f(a_208) = 208 - 10 = 198
f_a_candidate = CANDIDATE - 10
assert f_a_candidate == f_m, f"f(a_{CANDIDATE}) = {f_a_candidate}, f({m}) = {f_m} 불일치"

# 검증 7: f(a_k) ≤ f(m)을 만족하는 최댓값 확인
# k = CANDIDATE + 1 = 209일 때 f(a_209) = 199 > 198 = f(m)
f_a_next = (CANDIDATE + 1) - 10
assert f_a_next > f_m, f"f(a_{CANDIDATE+1}) = {f_a_next}는 f({m}) = {f_m}을 초과하지 않음"

# 최종 판정: f(a_k) ≤ f(m)을 만족하는 k의 최댓값 = CANDIDATE
if (f_a_candidate <= f_m) and (f_a_next > f_m):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")