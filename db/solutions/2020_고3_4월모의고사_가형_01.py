from sympy import cbrt, Rational, simplify
a = cbrt(9) * (3**Rational(1,3))
result = simplify(a)
print('VERIFY_PASS' if result == 3 else 'VERIFY_FAIL')