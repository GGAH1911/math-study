import sympy as sp
x = sp.Symbol('x')

# 우변 인수분해 확인
rhs = x**2 - 3*x + 2
factored = sp.factor(rhs)
assert factored == (x-1)*(x-2), f"우변 인수분해 실패: {factored}"

# x≠1일 때 f(x) = x-2
f_general = x - 2

# 조건 검증: (x-1)f(x) = x^2 - 3x + 2
lhs_expr = (x-1) * f_general
verify_general = sp.simplify(lhs_expr - rhs)
assert verify_general == 0, f"x≠1일 때 조건 불만족: {verify_general}"

# 연속성: f(1) = lim(x→1) f(x) = lim(x→1) (x-2)
f_1_limit = sp.limit(f_general, x, 1)
assert f_1_limit == -1, f"극한값 오류: {f_1_limit}"

# x=1에서 원래 조건 확인: (x-1)f(x) = x^2 - 3x + 2
# x=1일 때 좌변: (1-1)*(-1) = 0
# x=1일 때 우변: 1-3+2 = 0
lhs_at_1 = (1-1)*(-1)
rhs_at_1 = 1 - 3 + 2
assert lhs_at_1 == rhs_at_1 == 0, f"x=1에서 조건 불만족: {lhs_at_1} ≠ {rhs_at_1}"

print('VERIFY_PASS')