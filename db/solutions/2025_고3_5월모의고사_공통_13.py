import sympy as sp

x = sp.Symbol('x')

# 원래 문제 조건 설정
# f(x): 최고차항 계수 1인 이차함수, 우리가 구한 답 f(x) = x^2 - 5x + 2
f = x**2 - 5*x + 2
line = x - 3

# 교점 확인 (y = f(x) 와 y = x-3)
diff = f - line  # (x-1)(x-5)
roots = sp.solve(diff, x)
alpha, beta = sorted(roots)

assert alpha == 1 and beta == 5, f'roots wrong: {roots}'
assert 0 < alpha < 3 < beta, 'x-coordinate condition failed'

# C = (0, -3)
C = (0, -3)
assert line.subs(x, 0) == -3, 'C check failed'

# S1 계산
S1 = sp.integrate(f - line, (x, 0, alpha))
assert S1 > 0, f'S1 should be positive, got {S1}'

# S2 계산
S2 = sp.integrate(line - f, (x, alpha, beta))
assert S2 > 0, f'S2 should be positive, got {S2}'

# 조건 S2 - 2*S1 = 6 검증
cond1 = sp.simplify(S2 - 2*S1 - 6)
assert cond1 == 0, f'S2-2S1=6 failed: {S2-2*S1}'

# x=3 이등분 조건 검증
left_area = sp.integrate(line - f, (x, alpha, 3))
right_area = sp.integrate(line - f, (x, 3, beta))
assert sp.simplify(left_area - right_area) == 0, f'bisection failed: {left_area} vs {right_area}'

# 최고차항 계수 1 확인
assert f.coeff(x, 2) == 1, 'leading coeff not 1'

# f(-1) 확인
result = f.subs(x, -1)
assert result == 8, f'f(-1) = {result}, expected 8'

print('VERIFY_PASS')
