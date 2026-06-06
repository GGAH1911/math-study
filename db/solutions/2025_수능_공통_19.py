from sympy import symbols, diff, solve, simplify, Rational

CANDIDATE = '41'

x, a = symbols('x a', real=True, positive=True)

# 문제에서 주어진 함수: f(x) = 2x^3 - 3ax^2 - 12a^2*x
f = 2*x**3 - 3*a*x**2 - 12*a**2*x

# 도함수를 구해 극값점 찾기
f_prime = diff(f, x)  # f'(x) = 6x^2 - 6ax - 12a^2
critical_points = solve(f_prime, x)  # x = -a, 2a

# 극댓값은 x = -a에서 발생
f_max = f.subs(x, -a)  # f(-a) = 7a^3

# 극댓값 조건 f(-a) = 7/27에서 a를 구하기
a_val = solve(f_max - Rational(7, 27), a)[0]  # a = 1/3

# f(3) 계산
result = int(simplify(f.subs([(x, 3), (a, a_val)])))

# 정답 검증: result가 CANDIDATE와 같은지 원래 조건에서 확인
print("VERIFY_PASS" if result == int(CANDIDATE) else "VERIFY_FAIL")