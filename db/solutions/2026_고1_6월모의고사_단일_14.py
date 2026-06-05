import numpy as np
from sympy import symbols, expand, solve

a = 2
P = lambda x: x**4 - 4*x**3 - a**4 + 4*a**3
print('P(2):', P(2))
print('P(-2):', P(-2))
print('VERIFY_PASS' if abs(P(2)) < 1e-10 else 'VERIFY_FAIL')