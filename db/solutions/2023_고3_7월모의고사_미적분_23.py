import sympy as sp
from sympy import symbols, sqrt, limit, oo

n = symbols('n', positive=True, integer=True)
expr = 2*n*(sqrt(n**2 + 4) - sqrt(n**2 + 1))
result = limit(expr, n, oo)
if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')