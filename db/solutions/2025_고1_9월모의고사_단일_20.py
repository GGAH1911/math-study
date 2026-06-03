import sympy as sp
from sympy import symbols, expand, solve

x = symbols('x')

# 구한 함수들
f = -x**2 + 7
g = -x**2 + 16*x - 41

# 조건 (가) 검증: h(x) = f(0) = 7의 해가 0, 4, 12
f_val_0 = f.subs(x, 0)
roots_f = solve(f - f_val_0, x)
roots_g = solve(g - f_val_0, x)
all_roots = sorted(list(set([0] + [r for r in roots_g if r > 3])))
assert all_roots == [0, 4, 12], f'조건 (가) 실패: {all_roots}'

# 조건 (나) 검증: h(x) = 2x - 8의 해가 -5, 3, 11
line = 2*x - 8
roots_f_line = solve(f - line, x)
roots_g_line = solve(g - line, x)
f_solutions = [r for r in roots_f_line if r <= 3]
g_solutions = [r for r in roots_g_line if r > 3]
all_line_roots = sorted(f_solutions + g_solutions)
assert set(all_line_roots) == {-5, 3, 11}, f'조건 (나) 실패: {all_line_roots}'

# 답 검증
h_neg2 = f.subs(x, -2)
h_5 = g.subs(x, 5)
answer = h_neg2 + h_5
assert answer == 17, f'답 검증 실패: {answer}'

print('VERIFY_PASS')