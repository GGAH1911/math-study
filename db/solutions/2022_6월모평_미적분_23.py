import sympy as sp
import numpy as np
from sympy import symbols, sqrt, limit, oo

n = symbols('n')
expr = 1 / (sqrt(n**2 + n + 1) - n)
result = limit(expr, n, oo)
print(f'Limit result: {result}')
if result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')