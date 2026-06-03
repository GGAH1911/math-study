from fractions import Fraction
import sympy as sp

expr = sp.Rational(54)**sp.Rational(1,3) * 2**sp.Rational(5,3)
result = sp.simplify(expr)
if result == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)
