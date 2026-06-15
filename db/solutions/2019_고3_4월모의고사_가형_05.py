from sympy import symbols, diff, solve, simplify, Rational

a = symbols('a', positive=True, real=True)
f = lambda x: 1 / (x - 2)

# 도함수 정의를 사용한 미분
f_prime_a = diff(f(a), a)

# 주어진 조건: f'(a) = -1/4
condition = f_prime_a + Rational(1, 4)

# a를 풀기
solutions = solve(condition, a)

# 양수 해 찾기
positive_solutions = [sol for sol in solutions if sol > 0]

# 검증
if positive_solutions:
    a_val = positive_solutions[0]
    derivative_at_a = f_prime_a.subs(a, a_val)
    if abs(derivative_at_a + Rational(1, 4)) < 1e-10 or derivative_at_a == -Rational(1, 4):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')