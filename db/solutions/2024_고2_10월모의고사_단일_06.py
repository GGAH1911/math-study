from sympy import symbols, solve, Rational

a1 = symbols('a1')
d = 3

a2 = a1 + d
a4 = a1 + 3*d

# 원래 조건: a2 * a4 = 72
eq = a2 * a4 - 72
solutions = solve(eq, a1)

# 첫째항 양수 조건
valid = [s for s in solutions if s > 0]
assert len(valid) == 1, 'VERIFY_FAIL: 양수 해가 1개가 아님'

a1_val = valid[0]
a3_val = a1_val + 2*d

# 답 검증
assert a3_val == 9, f'VERIFY_FAIL: a3 = {a3_val}'

# 원래 조건도 재확인
a2_val = a1_val + d
a4_val = a1_val + 3*d
assert a2_val * a4_val == 72, 'VERIFY_FAIL: a2*a4 != 72'

print('VERIFY_PASS')
