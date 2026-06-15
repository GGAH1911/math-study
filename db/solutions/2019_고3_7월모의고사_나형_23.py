CANDIDATE = 12

import sympy as sp

x = sp.Symbol('x')
f = x**4 - 5*x**2 + 9
f_prime = sp.diff(f, x)
result = f_prime.subs(x, 2)

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')