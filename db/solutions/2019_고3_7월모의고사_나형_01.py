from sympy import Rational, simplify
result = 3 * (27 ** Rational(1, 3))
result = simplify(result)
if result == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')