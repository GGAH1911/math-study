CANDIDATE = '24'

from sympy import symbols, integrate, simplify

x, t = symbols('x t', real=True)

# 주어진 함수방정식: 2x^2 * f(x) = 3 * ∫[0,x] (x-t) * {f(x) + f(t)} dt
# 조건: f'(2) = 4
# 구하는 값: f(6)

# 검증된 풀이로부터 유도된 함수: f(x) = 4x

# ===== 함수방정식 검증 =====
# f(x) = 4x, f(t) = 4t를 대입

# 좌변: 2x^2 * f(x)
f_x = 4 * x
lhs = 2 * x**2 * f_x

# 우변: 3 * ∫[0,x] (x-t) * {f(x) + f(t)} dt
f_t = 4 * t
integrand = (x - t) * (f_x + f_t)
integral = integrate(integrand, (t, 0, x))
rhs = 3 * integral

# 함수방정식 만족 확인
equation_satisfied = (simplify(lhs - rhs) == 0)

# ===== 조건 검증 =====
# f(x) = 4x이므로 f'(x) = 4
# f'(2) = 4 ✓
condition_satisfied = (4 == 4)

# ===== 답 계산 및 검증 =====
# f(6) = 4 * 6 = 24
f_6_value = 4 * 6
answer_matches = (f_6_value == int(CANDIDATE))

# ===== 최종 판정 =====
if equation_satisfied and condition_satisfied and answer_matches:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")