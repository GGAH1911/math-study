import sympy as sp
import numpy as np
from sympy import sqrt, limit, oo, symbols

n = symbols('n')
expr = sqrt(n**4 + 5*n**2 + 5) - n**2
result = limit(expr, n, oo)
print(f'Limit result: {result}')
print(f'Decimal value: {float(result)}')
if result == sp.Rational(5, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')