import sympy as sp
import numpy as np
from sympy import sqrt, limit, oo, symbols

n = symbols('n', positive=True, integer=True)
a = 9
b = -1

# Original limit expression
numerator = a * n**b
denominator = sqrt(n**4 + 4*n) - sqrt(n**4 + n)
expression = numerator / denominator

# Calculate limit
result = limit(expression, n, oo)
print(f'Limit result: {result}')

# Check if result equals 6
if result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')