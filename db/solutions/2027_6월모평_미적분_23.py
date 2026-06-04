import sympy as sp
from sympy import symbols, limit, oo

n = symbols('n')
expr = (4 * 5**n - 2**(n+1)) / (5**n + 2**n)
result = limit(expr, n, oo)
print('VERIFY_PASS' if result == 4 else f'VERIFY_FAIL: {result}')