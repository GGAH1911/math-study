from sympy import Rational, Symbol, solve
PAc = Rational(2,5)
PB = Rational(1,6)
PA = 1 - PAc
# independence: P(A and B) = P(A)P(B)
PAB = PA * PB
# De Morgan: A^c U B^c = (A and B)^c
res = 1 - PAB
expected = Rational(9,10)
print('VERIFY_PASS' if res == expected else 'VERIFY_FAIL')