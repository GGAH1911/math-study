from sympy import *
x = symbols('x')
f = (exp(5*x) - 1) / (3*x)
limit_value = limit(f, x, 0)
print(f'극한값: {limit_value}')
if limit_value == Rational(5, 3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')