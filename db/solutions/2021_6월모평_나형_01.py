from sympy import cbrt, simplify, Rational
expr = cbrt(8) * 4**Rational(3,2)
result = simplify(expr)
if result == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')