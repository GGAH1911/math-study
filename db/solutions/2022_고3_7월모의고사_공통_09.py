from sympy import symbols, integrate, diff
a, b = -3, 2
def f_prime(x):
    return 3*x**2 + 2*a*x + b

# 검증: 조건 확인
int1 = integrate(f_prime(symbols('x')), (symbols('x'), 0, 1))
int2 = integrate(f_prime(symbols('x')), (symbols('x'), 0, 2))
ans = f_prime(1)

if int1 == 0 and int2 == 0 and ans == -1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')