import sympy as sp
from sympy import symbols, diff, integrate

CANDIDATE = 12

x = symbols('x')
f_prime = 3*x**2 + 4*x + 5
f = integrate(f_prime, x) + 4

f_at_0 = f.subs(x, 0)
f_at_1 = f.subs(x, 1)

f_prime_check = diff(f, x)

if f_at_0 == 4 and f_prime_check == f_prime and f_at_1 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')