import math
from sympy import cbrt, sympify

answer = 32
original_expr = cbrt(2**3 * 16**3)
result = float(original_expr)

if abs(result - answer) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')