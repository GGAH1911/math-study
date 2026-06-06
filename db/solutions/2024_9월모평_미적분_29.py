import sympy as sp
n = sp.Symbol('n', integer=True, positive=True)
a_val = 9
b_val = 9

# 첫 번째 극한
lim1_expr = (3**n + a_val**(n+1)) / (3**(n+1) + a_val**n)
lim1 = sp.limit(lim1_expr, n, sp.oo)
print(f'첫 번째 극한: {lim1} (기댓값: {a_val})')
assert lim1 == a_val, f'첫 번째 극한 실패: {lim1} != {a_val}'

# 두 번째 극한
lim2_expr = (a_val**n + b_val**(n+1)) / (a_val**(n+1) + b_val**n)
lim2 = sp.limit(lim2_expr, n, sp.oo)
expected_lim2 = sp.Rational(9, a_val)
print(f'두 번째 극한: {lim2} (기댓값: {expected_lim2})')
assert lim2 == expected_lim2, f'두 번째 극한 실패: {lim2} != {expected_lim2}'

print('VERIFY_PASS')