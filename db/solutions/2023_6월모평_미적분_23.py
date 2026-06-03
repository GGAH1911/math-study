import sympy as sp
import numpy as np
from sympy import symbols, sqrt, limit, oo

n = symbols('n', positive=True, real=True)
expr = 1 / (sqrt(n**2 + 3*n) - sqrt(n**2 + n))
limit_val = limit(expr, n, oo)
print(f'Limit value: {limit_val}')
print('VERIFY_PASS' if limit_val == 1 else 'VERIFY_FAIL')