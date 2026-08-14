from sympy import symbols, diff, Function, Eq
x = symbols('x')
f = symbols('f', cls=Function)
# f(x)를 일반 다항함수로 설정, f(1)=2, f'(1)=1 조건 사용
# g(x) = (x^2 + 2x)*f(x)에서 g'(x) = (2x+2)*f(x) + (x^2+2x)*f'(x)
# x=1에서 g'(1) = (2*1+2)*f(1) + (1^2+2*1)*f'(1)
# = 4*f(1) + 3*f'(1)
f_at_1 = 2
f_prime_at_1 = 1
g_prime_at_1 = 4 * f_at_1 + 3 * f_prime_at_1
if g_prime_at_1 == 11:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')