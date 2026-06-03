from sympy import *
h = symbols('h')
f = lambda x: x**2 + x + 2
f_2 = f(2)
f_2_plus_h = f(2 + h)
difference_quotient = (f_2_plus_h - f_2) / h
limit_result = limit(difference_quotient, h, 0)
if limit_result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')