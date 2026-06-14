CANDIDATE = 3

from sympy import symbols, limit, oo

n = symbols('n')
expr = n * (9*n - 5) / (3*n**2 + 1)
result = limit(expr, n, oo)

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')