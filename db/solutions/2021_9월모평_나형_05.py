from fractions import Fraction
P_A = Fraction(2, 5)
P_B = Fraction(4, 5)
P_AUB = Fraction(9, 10)
P_AandB = P_A + P_B - P_AUB
P_B_given_A = P_AandB / P_A
if P_B_given_A == Fraction(3, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')