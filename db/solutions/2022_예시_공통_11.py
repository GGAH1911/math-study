from sympy import symbols, expand, solve

x = symbols('x')
f = x**3 - 7*x**2 + 14*x + 1

# 조건 1: f(0) = 1
assert f.subs(x, 0) == 1, 'f(0) should be 1'

# 조건 2: f'(2) = -2
fprime = 3*x**2 - 14*x + 14
assert fprime.subs(x, 2) == -2, 'f\'(2) should be -2'

# 조건 3: f(x) = 9의 근이 1, 2, 4인지 확인
eq = f - 9
roots = solve(eq, x)
assert set(roots) == {1, 2, 4}, 'Roots of f(x)=9 should be 1, 2, 4'

# 세 근이 등비수열인지 확인 (1, 2, 4)
assert 2/1 == 4/2 == 2, 'Roots should form a geometric sequence'

# 답 검증
answer = f.subs(x, 3)
assert answer == 7, f'f(3) should be 7, got {answer}'

print('VERIFY_PASS')