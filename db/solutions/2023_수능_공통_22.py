from sympy import symbols, sqrt, simplify, expand, Rational

CANDIDATE = '13'

x = symbols('x', real=True)

# ===== 문제에서 주어진 함수 정의 =====
# 최고차항의 계수가 1인 삼차함수 f(x)
# 검증된 풀이: f(x) = x^3 - 6x^2 + 12x - 3
f_expr = x**3 - 6*x**2 + 12*x - 3

# 실수 전체에서 연속인 함수 g(x)
# 검증된 풀이: g(x) = 2 + sqrt((x^2 - 5x + 7)/3)
g_expr = 2 + sqrt((x**2 - 5*x + 7) / 3)

# ===== 각 조건 검증 =====
all_conditions_met = True

# 조건 (다) 검증: f(0) = -3, f(g(1)) = 6
f_at_0 = f_expr.subs(x, 0)
condition_da = (f_at_0 == -3)
print(f"조건 (다)-1: f(0) = {f_at_0}, 예상값 = -3, 일치 = {condition_da}")
all_conditions_met = all_conditions_met and condition_da

g_at_1 = simplify(g_expr.subs(x, 1))
f_at_g1 = simplify(f_expr.subs(x, g_at_1))
condition_db = (f_at_g1 == 6)
print(f"조건 (다)-2: g(1) = {g_at_1}, f(g(1)) = {f_at_g1}, 예상값 = 6, 일치 = {condition_db}")
all_conditions_met = all_conditions_met and condition_db

# 조건 (나) 검증: g(x)의 최솟값 = 5/2
# x^2 - 5x + 7의 최솟값 = 3/4 (at x = 5/2)
# g_min = 2 + sqrt((3/4)/3) = 2 + sqrt(1/4) = 2.5 = 5/2
g_min = 2 + sqrt(Rational(3, 4) / 3)
g_min_simplified = simplify(g_min)
condition_b = (g_min_simplified == Rational(5, 2))
print(f"조건 (나): g(x)의 최솟값 = {g_min_simplified}, 예상값 = 5/2, 일치 = {condition_b}")
all_conditions_met = all_conditions_met and condition_b

# 조건 (가) 검증: 모든 실수 x에 대해 f(x) = f(1) + (x-1)f'(g(x))
# 즉, f(x) - f(1) = (x-1) * f'(g(x))
f_at_1 = f_expr.subs(x, 1)  # f(1) = 4

# 좌변: f(x) - f(1)
lhs = expand(f_expr - f_at_1)  # x^3 - 6x^2 + 12x - 7

# 우변: (x-1) * f'(g(x))
# f'(t) = 3t^2 - 12t + 12 = 3(t-2)^2
# (g(x) - 2)^2 = (x^2 - 5x + 7)/3이므로
# f'(g(x)) = 3(g(x)-2)^2 = x^2 - 5x + 7
f_prime_g = 3 * simplify((g_expr - 2)**2)
f_prime_g_simplified = simplify(f_prime_g)
rhs = expand((x - 1) * f_prime_g_simplified)

# 조건 확인: 좌변 = 우변인지 검증
condition_a = (simplify(expand(lhs - rhs)) == 0)
print(f"조건 (가): f(x)-f(1) = {lhs}")
print(f"         (x-1)f'(g(x)) = {rhs}")
print(f"         일치 = {condition_a}")
all_conditions_met = all_conditions_met and condition_a

# ===== 최종 답 계산 및 검증 =====
f_at_4 = f_expr.subs(x, 4)
print(f"\n최종 계산:")
print(f"f(4) = {f_at_4}")
print(f"CANDIDATE = '{CANDIDATE}'")

# 숫자로 변환
f_at_4_int = int(f_at_4)
candidate_int = int(CANDIDATE)

if all_conditions_met and f_at_4_int == candidate_int:
    print("\nVERIFY_PASS")
else:
    print("\nVERIFY_FAIL")