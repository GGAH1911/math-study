from sympy import log, Rational, simplify, nsimplify
expr = log(10, 3) + log(Rational(9,5), 3) - log(Rational(2,3), 3)
val = simplify(expr)
if simplify(val - 3) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')