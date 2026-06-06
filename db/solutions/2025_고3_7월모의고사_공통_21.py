from sympy import symbols, integrate, Rational

CANDIDATE = '28'

# 원래 함수: f(x) = -x^2 + kx
# 점 A(a, f(a))에서의 접선: g(x) = (-2a+k)x + a^2
# 조건 (가): ∫_a^b g(x)dx = S (b: x절편, S: 삼각형 AOH의 넓이)
# 조건 (나): 4k^3/81 = 32/3

# 검증된 풀이로부터
k = 6
a = 4

def f(x):
    return -x**2 + k*x

def f_prime(x):
    return -2*x + k

def g(x):
    return (-2*a + k)*x + a**2

# 접선이 점 A(a, f(a))를 지나는가
assert g(a) == f(a), '점 A를 지나지 않음'

# x절편 b = a^2 / (2a - k)
b = a**2 / (2*a - k)
assert b == 8, f'x절편: {b}'

# 삼각형 AOH의 넓이: S = a^2(k-a)/2
S = a**2 * (k - a) / 2
assert S == 16, f'넓이: {S}'

# 조건 (가): ∫_a^b g(x)dx = S
x = symbols('x')
g_expr = (-2*a + k)*x + a**2
integral = integrate(g_expr, (x, a, b))
assert integral == S, f'조건 (가): {integral} != {S}'

# 조건 (나): 4k^3/81 = 32/3
lhs = Rational(4 * k**3, 81)
rhs = Rational(32, 3)
assert lhs == rhs, f'조건 (나): {lhs} != {rhs}'

# 최종 답: g(-6)
result = g(-6)

# CANDIDATE 검증
try:
    candidate_val = int(CANDIDATE)
except (ValueError, TypeError):
    print('VERIFY_FAIL')
    exit()

if result == candidate_val:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')