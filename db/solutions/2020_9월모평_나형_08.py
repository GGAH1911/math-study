from sympy import Rational
P_A = Rational(7,10)
P_AuB = Rational(9,10)
# P(B^C and A^C) = P((A u B)^C) = 1 - P(A u B)
num = 1 - P_AuB
# P(A^C) = 1 - P(A)
den = 1 - P_A
ans = num/den
expected = Rational(1,3)
print('VERIFY_PASS' if ans == expected else 'VERIFY_FAIL')