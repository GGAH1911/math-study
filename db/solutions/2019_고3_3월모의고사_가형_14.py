from sympy import symbols, diff, solve, Rational

x = symbols('x')
f = x**3 - 5*x**2 + 9*x - 5

# f(x) = 4를 풀어 g(4) 구하기
solutions = solve(f - 4, x)
g_4 = [sol for sol in solutions if sol.is_real][0]

# f'(x) 계산
f_prime = diff(f, x)

# f'(g(4)) 계산
f_prime_at_g4 = f_prime.subs(x, g_4)

# g'(4) = 1/f'(g(4))
g_prime_4 = 1 / f_prime_at_g4

# 검증: g'(4)이 1/6인지 확인
if g_prime_4 == Rational(1, 6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')