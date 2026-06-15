from sympy import Rational
PA = Rational(2,5)
PBc = Rational(3,10)
PAB = Rational(1,5)
PB = 1 - PBc
PAuB = PA + PB - PAB
PAcBc = 1 - PAuB
ans = PAcBc / PBc
if ans == Rational(1,3):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')