from sympy import symbols, solve, simplify
k, a, x = symbols('k a x', real=True)
# 점근선 교점 조건
a_val = solve(5 - (2*a + 1), a)[0]
assert a_val == 2
# 점을 지나는 조건
k_val = solve(6 - (k/(5-1) + 5), k)[0]
assert k_val == 4
# 검증
y_at_5 = k_val/(5-1) + 5
assert y_at_5 == 6
print('VERIFY_PASS')