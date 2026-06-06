import sympy as sp
x = sp.Symbol('x')

# 정의한 함수
f = (1/4)*(x - 2)**2 - 5/4
g = -(1/2)*(x - 1)**2 + 1

# 조건 검증
# X: |f(x)| = 1의 근
roots_f1 = sp.solve(f - 1, x)
roots_f_minus1 = sp.solve(f + 1, x)
X = sorted(roots_f1 + roots_f_minus1)

# Y: |g(x)| = 1의 근
roots_g1 = sp.solve(g - 1, x)
roots_g_minus1 = sp.solve(g + 1, x)
Y = sorted(roots_g1 + roots_g_minus1)

# 집합 연산
X_set = set(X)
Y_set = set(Y)
X_intersect_Y = sorted(list(X_set & Y_set))
X_union_Y = sorted(list(X_set | Y_set))

# 조건 확인
assert len(X_intersect_Y) == 3, f'n(X∩Y) = {len(X_intersect_Y)}, 3이어야 함'
assert len(X_union_Y) == 4, f'n(X∪Y) = {len(X_union_Y)}, 4여야 함'
assert abs(sum(X_intersect_Y) - 3) < 1e-9, f'sum(X∩Y) = {sum(X_intersect_Y)}, 3이어야 함'
assert abs(sum(X_union_Y) - 8) < 1e-9, f'sum(X∪Y) = {sum(X_union_Y)}, 8이어야 함'

# f(2) < f(1) 확인
f_at_2 = float(f.subs(x, 2))
f_at_1 = float(f.subs(x, 1))
assert f_at_2 < f_at_1, f'f(2)={f_at_2}, f(1)={f_at_1}, f(2) < f(1)이어야 함'

# 최종 답
f_at_7 = float(f.subs(x, 7))
g_at_9 = float(g.subs(x, 9))
result = f_at_7 - g_at_9

assert abs(result - 36) < 1e-9, f'f(7) - g(9) = {result}, 36이어야 함'
print('VERIFY_PASS')