from sympy import Rational, simplify
# Given conditions
PAc = Rational(2,3)          # P(A^C)
PAcB = Rational(1,4)         # P(A^C ∩ B)
PA = 1 - PAc                 # P(A)
# A ∪ B = A ∪ (A^C ∩ B), disjoint -> P(A∪B) = P(A) + P(A^C∩B)
PAuB = PA + PAcB
expected = Rational(7,12)
if simplify(PAuB - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')