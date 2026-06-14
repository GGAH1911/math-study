from sympy import Rational
PAc = Rational(2,5)
PB = Rational(2,5)
PA = 1 - PAc
# independence
PAB = PA*PB
Punion = PA + PB - PAB
expected = Rational(19,25)
print('VERIFY_PASS' if Punion == expected else 'VERIFY_FAIL')