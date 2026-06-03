import sympy as sp
from sympy import exp, limit, symbols

x = symbols('x')
f = (exp(x) - exp(1)) / (x - 1)
result = limit(f, x, 1)
print('VERIFY_PASS' if result == exp(1) else 'VERIFY_FAIL')