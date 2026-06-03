import sympy as sp

# 주어진 조건
f_0 = -1
f_prime_0 = 3

# g(x) = (x+2)f(x)에서 곱의 미분
# g'(x) = f(x) + (x+2)f'(x)
# g'(0) = f(0) + 2*f'(0)

g_prime_0 = f_0 + 2 * f_prime_0

if g_prime_0 == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')