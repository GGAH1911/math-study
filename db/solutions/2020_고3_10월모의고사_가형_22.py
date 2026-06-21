import numpy as np
from sympy import *

CANDIDATE = 3

x = symbols('x')
f = sin(3*x - 6)
f_prime = diff(f, x)
result = f_prime.subs(x, 2)
result_numeric = float(result)

if abs(result_numeric - CANDIDATE) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')