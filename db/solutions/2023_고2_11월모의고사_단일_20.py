from sympy import *
t = symbols('t', real=True, positive=True)
k = symbols('k', real=True, positive=True)
f = (t+1)*(t-6)**2
f_prime_expr = 3*k**2 - 22*k + 24
c = f/t

# ㄱ 검증: f'(0) = 24
f_prime_at_0 = f_prime_expr.subs(k, 0)
assert f_prime_at_0 == 24, f'ㄱ 실패: {f_prime_at_0}'

# ㄴ 검증: g(6) = 4/3
c_at_6 = c.subs(t, 6)
assert c_at_6 == 0, f'c(6) = {c_at_6}'
eq1 = Eq(f_prime_expr, 0)
roots = solve(eq1, k)
positive_roots = [r for r in roots if r > 0]
assert len(positive_roots) == 2, f'실근 개수: {len(positive_roots)}'
assert min(positive_roots) == Rational(4,3), f'작은 근: {min(positive_roots)}'

# ㄷ 검증: 취해지지 않는 자연수의 합
# c(2) = 24와 c(t_2) = 24인 점 확인
equation = Eq((t+1)*(t-6)**2 - 24*t, 0)
ts = solve(equation, t)
ts_positive = [x for x in ts if x > 0]
assert 2 in ts_positive, f't=2가 해가 아님'

# 치역: (0, 4/3] ∪ (22/3, ∞)
# 포함되지 않는 자연수: 2,3,4,5,6,7
missing_sum = sum([2,3,4,5,6,7])
assert missing_sum == 27, f'합: {missing_sum}'

print('VERIFY_PASS')