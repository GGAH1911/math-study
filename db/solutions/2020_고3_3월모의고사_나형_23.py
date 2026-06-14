from sympy import symbols, diff

CANDIDATE = 19

x = symbols('x')
f = x**4 + 3*x**2 + 9*x - 27

# f'(x) 구하기
f_prime = diff(f, x)

# f'(1) 계산
f_prime_at_1 = f_prime.subs(x, 1)

if f_prime_at_1 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')