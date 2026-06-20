from sympy import Rational, simplify
PB = Rational(1,3)
PAB = Rational(1,6)
PAuB = Rational(1,1)
# P(A) from inclusion-exclusion
PA = PAuB - PB + PAB
PAc = 1 - PA
# check consistency: recompute union
union_check = PA + PB - PAB
if simplify(union_check - 1) == 0 and PAc == Rational(1,6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')