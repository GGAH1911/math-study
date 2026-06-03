import sympy as sp

# 변수 정의
x = sp.Symbol('x')
f = sp.Function('f')

# 주어진 조건: f(2) = 1, f'(2) = 3
f_at_2 = 1
f_prime_at_2 = 3

# g(x) = x^2 * f(x)의 미분
# g'(x) = 2x*f(x) + x^2*f'(x)
# g'(2) = 2(2)*f(2) + 2^2*f'(2)

g_prime_at_2 = 2 * 2 * f_at_2 + 4 * f_prime_at_2
result = g_prime_at_2

# 검증
if result == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')