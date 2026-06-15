from sympy import Rational
P_AuB = Rational(3,4)
P_AcB = Rational(2,3)
# A and (A^C cap B) are disjoint and their union is A u B
P_A = P_AuB - P_AcB
expected = Rational(1,12)
# consistency check: probabilities valid and identity holds
ok = (P_A == expected) and (0 <= P_A <= 1) and (P_A + P_AcB == P_AuB)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
