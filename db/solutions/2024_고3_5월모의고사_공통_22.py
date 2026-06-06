from sympy import symbols, expand, integrate, Rational, simplify

CANDIDATE = 114

# 문제 조건으로부터 결정된 극점 위치
p1 = Rational(-1, 2)  # 첫 번째 극점
p2 = Rational(1, 2)   # 두 번째 극점 = a (h의 분기점)
p3 = 2                 # 세 번째 극점
a = Rational(1, 2)

# f'(x) = 16(x - p1)(x - p2)(x - p3) 형태
# f(x)는 최고차 계수 4인 사차함수
x = symbols('x')
f_prime = 16 * (x - p1) * (x - p2) * (x - p3)
f_prime = expand(f_prime)

# f(x)를 f'(x)에서 적분하여 구함
f_indefinite = integrate(f_prime, x)

# 초기조건 g(0) = 40/3
# 0 ∈ (p1, p2)이므로 g(0) = f(0), 따라서 C = 40/3
C = Rational(40, 3)
f_expr = f_indefinite + C

# ====== 검증: 주어진 조건들 ======

# 조건 1: g(0) = 40/3
g_at_0 = f_expr.subs(x, 0)
assert g_at_0 == Rational(40, 3), f"조건 실패: g(0) = {g_at_0} != 40/3"

# 조건 2: f(p3) = 0 (세 극값 중 한 극솟값이 0)
f_at_p3 = f_expr.subs(x, p3)
assert f_at_p3 == 0, f"조건 실패: f({p3}) = {f_at_p3} != 0"

# 조건 3: h(p1) = 0 (x = p1에서 g의 점프가 h=0에서 상쇄)
h_at_p1 = 4 * p1 + 2  # x < a일 때 h(x) = 4x + 2
assert h_at_p1 == 0, f"조건 실패: h({p1}) = {h_at_p1} != 0"

# 조건 4: g(x)h(x)가 x = a에서 연속
# x < a: g(a-) = f(a), h(a-) = 4a+2
# x >= a: g(a+) = -f(a), h(a+) = -2a-3
f_at_a = f_expr.subs(x, a)
h_minus = 4 * a + 2      # = 4
h_plus = -2 * a - 3     # = -4
product_left = f_at_a * h_minus
product_right = (-f_at_a) * h_plus
assert product_left == product_right, f"연속성 실패: {product_left} != {product_right}"

# ====== 최종 답 계산 ======

# f(1) 계산
f_at_1 = f_expr.subs(x, 1)

# 1 ∈ (p2, p3) = (1/2, 2)이고 이 구간에서 f'(x) < 0
# 따라서 |g(x)| = f(x)이고 g'_+ = |f'|이므로 g(1) = -f(1)
g_at_1 = -f_at_1

# h(3): 3 >= a = 1/2이므로 h(3) = -2(3) - 3
h_at_3 = -2 * 3 - 3

# g(1) × h(3) 계산
result = simplify(g_at_1 * h_at_3)

# 최종 검증: CANDIDATE와 일치하는가?
if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")