from sympy import symbols, diff, Function
x = symbols('x')
f = Function('f')
# 주어진 조건: f(1) = 2, f'(1) = 1
f_at_1 = 2
f_prime_at_1 = 1

# g'(x) = 2x*f(x) + (x^2+3)*f'(x)
# g'(1) = 2*1*f(1) + (1^2+3)*f'(1)
g_prime_at_1 = 2*1*f_at_1 + (1**2 + 3)*f_prime_at_1
result = g_prime_at_1

if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')