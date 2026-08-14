from sympy import *
x = symbols('x')
f = tan(6*x) / (exp(2*x) - 1)
limit_val = limit(f, x, 0)
if limit_val == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')