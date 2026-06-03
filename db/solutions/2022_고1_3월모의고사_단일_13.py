from sympy import symbols, solve, simplify

x, k = symbols('x k', real=True)

# 첫 번째 방정식의 해
eq1 = x**2 - x - 2
roots_eq1 = solve(eq1, x)
# roots_eq1 = [-1, 2]

# 두 번째 방정식
eq2 = 2*x**2 + k*x - 6

# 각 근을 두 번째 식에 대입해서 k값 구하기
k_values = []
for root in roots_eq1:
    eq2_at_root = eq2.subs(x, root)
    k_sol = solve(eq2_at_root, k)
    k_values.extend(k_sol)

k_values = list(set(k_values))  # 중복 제거

# k_values = [-4, -1]
# 검증: 각 k에 대해 실제로 공통인 해가 있는지 확인
for k_val in k_values:
    eq2_specific = 2*x**2 + k_val*x - 6
    roots_eq2 = solve(eq2_specific, x)
    common_roots = set(roots_eq1) & set(roots_eq2)
    assert len(common_roots) > 0, f'k={k_val}일 때 공통인 해 없음'

# 모든 k값의 합
k_sum = sum(k_values)
assert k_sum == -5, f'합이 {k_sum}이지만 -5여야 함'

print('VERIFY_PASS')