from sympy import Rational, Integer

expr = (Integer(4) ** Rational(1, 3)) ** 2 * Integer(2) ** Rational(2, 3)
result = expr
print('VERIFY_PASS' if result == 4 else f'VERIFY_FAIL: got {result}')