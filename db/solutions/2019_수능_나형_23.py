import sympy as sp

CANDIDATE = 20

x = sp.Symbol('x')
f = x**4 - 3*x**2 + 8
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 2)

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')