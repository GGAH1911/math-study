from sympy import symbols, diff

CANDIDATE = 112

x = symbols('x')
f = 10*x**2 + 12*x
f_prime = diff(f, x)
f_prime_at_5 = f_prime.subs(x, 5)

if f_prime_at_5 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')