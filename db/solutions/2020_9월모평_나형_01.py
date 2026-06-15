from sympy import *
result = 3**3 / (81**(Rational(1,2)))
print('VERIFY_PASS' if result == 3 else f'VERIFY_FAIL: {result}')