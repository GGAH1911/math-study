from sympy import *
x = symbols('x')
f = (exp(2*x) + exp(3*x) - 2) / (2*x)
limit_result = limit(f, x, 0)
if limit_result == Rational(5, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')