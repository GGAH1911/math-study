import sympy as sp

CANDIDATE = 17

x = sp.Symbol('x')
f = x**4 + 3*x**2 + 7*x
f_prime = sp.diff(f, x)
f_prime_at_1 = f_prime.subs(x, 1)

if f_prime_at_1 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')