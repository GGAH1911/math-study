from sympy import *
n = symbols('n')
expr = (n**2 * (12*n + 1)) / (4*n**3 - 1)
limit_result = limit(expr, n, oo)
if limit_result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')