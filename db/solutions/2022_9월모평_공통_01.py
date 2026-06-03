from fractions import Fraction
result = Fraction(1,3)**Fraction(1,4) * Fraction(1, 1) / Fraction(1,1)
# 직접 계산
import sympy as sp
expr = sp.Rational(1,1) / sp.Rational(3)**sp.Rational(1,4) * 3**sp.Rational(-7,4)
val = sp.simplify(expr)
expected = sp.Rational(1, 9)
if val == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', val)