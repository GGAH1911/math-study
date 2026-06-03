import sympy as sp
x = sp.Symbol('x')
f_sym = sp.Function('f')
# 원래 조건: f(1) = 5, g(x) = (x^2 - 1)f(x)
# g'(x)를 구하기 위해 f를 구체적으로 정의
# f(1) = 5를 만족하는 다항함수 예: f(x) = 5 (상수함수)
f = lambda x_val: 5
f_prime = lambda x_val: 0

# g(x) = (x^2 - 1)f(x)이므로
# g'(1) = 2*1*f(1) + (1^2-1)*f'(1) = 2*5 + 0 = 10
g_prime_at_1 = 2*1*f(1) + (1**2 - 1)*f_prime(1)
if g_prime_at_1 == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')