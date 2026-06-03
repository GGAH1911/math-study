import sympy as sp
from sympy import limit, oo, Symbol

n = Symbol('n')
expr = (4 * 3**(n+1)) / (2**n + 3**n)
result = limit(expr, n, oo)
print('VERIFY_PASS' if result == 12 else f'VERIFY_FAIL: {result}')