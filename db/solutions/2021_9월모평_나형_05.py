from sympy import Rational
PA = Rational(2,5)
PB = Rational(4,5)
PAuB = Rational(9,10)
PAnB = PA + PB - PAuB
PB_given_A = PAnB / PA
if PB_given_A == Rational(3,4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')