from sympy import *
n = symbols('n')
expr = (8*n**2 - 3) / (2*n**2 + 7*n - 9)
limit_value = limit(expr, n, oo)
if limit_value == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')