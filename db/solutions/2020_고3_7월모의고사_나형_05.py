from sympy import Rational
PA = Rational(7,12)
PA_int_Bc = Rational(1,6)
# A = (A and B) disjoint union (A and B^C)
PA_int_B = PA - PA_int_Bc
expected = Rational(5,12)
# verify decomposition consistency: P(A and B) + P(A and B^C) == P(A)
if PA_int_B + PA_int_Bc == PA and PA_int_B == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
