CANDIDATE = 2

from sympy import *

x = symbols('x')
expr = x * cos(pi - x)
result = integrate(expr, (x, 0, pi))

if simplify(result) == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')