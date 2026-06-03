from sympy import sqrt, simplify, Rational
result = (-sqrt(2))**4 * 8**Rational(-2, 3)
result_simplified = simplify(result)
if result_simplified == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')