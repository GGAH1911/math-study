from sympy import *
x = symbols('x')
expr = 6*x / (exp(4*x) - exp(2*x))
limit_value = limit(expr, x, 0)
if limit_value == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')