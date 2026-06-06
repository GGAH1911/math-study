from fractions import Fraction
result = Fraction(6, 1) / Fraction(-4, 1) - (Fraction(5, 2) * Fraction(-3, 1))
if result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')