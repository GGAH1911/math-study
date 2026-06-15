from sympy import Rational
PA = Rational(1,6)
PB = Rational(2,3)
# A, B mutually exclusive => P(A and B) = 0
PAB = Rational(0)
# P(A^c and B) = P(B) - P(A and B)
ans = PB - PAB
expected = Rational(2,3)
print('VERIFY_PASS' if ans == expected else 'VERIFY_FAIL')