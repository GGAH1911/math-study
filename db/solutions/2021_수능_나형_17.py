from sympy import symbols, limit, diff, Function, oo
x = symbols('x')

# 조건을 만족하는 함수 설정
# f(x) = -3 + 6x + ax^2, g(x) = 3 - 3x + bx^2 (일반 형태)
# 단순화를 위해: f(x) = -3 + 6x, g(x) = 3 - 3x
f = lambda t: -3 + 6*t
g = lambda t: 3 - 3*t

# 조건 검증
lim1_num = f(x) + g(x)
lim1 = limit(lim1_num / x, x, 0)
print(f'조건 1 검증 (기댓값 3): {lim1}')

lim2_num = f(x) + 3
lim2_den = x * g(x)
lim2 = limit(lim2_num / lim2_den, x, 0)
print(f'조건 2 검증 (기댓값 2): {lim2}')

# h'(0) 계산
f0 = float(f(0))
g0 = float(g(0))
f_prime_0 = 6
g_prime_0 = -3

h_prime_0 = f_prime_0 * g0 + f0 * g_prime_0
print(f'h\'(0) = {f_prime_0} * {g0} + {f0} * {g_prime_0} = {h_prime_0}')

if h_prime_0 == 27:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')