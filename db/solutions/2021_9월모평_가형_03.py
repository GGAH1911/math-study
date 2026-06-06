from fractions import Fraction
P_A = Fraction(2, 5)
P_B = Fraction(4, 5)
P_AUB = Fraction(9, 10)
P_A_and_B = P_A + P_B - P_AUB
P_B_given_A = P_A_and_B / P_A
expected = Fraction(3, 4)
if P_B_given_A == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')