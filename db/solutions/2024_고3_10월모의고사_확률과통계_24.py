from fractions import Fraction
P_A = Fraction(2, 5)
P_B = Fraction(1, 6)
P_Ac = 1 - P_A
P_A_and_B = P_A * P_B
P_Ac_and_B = P_Ac * P_B
if P_A_and_B == Fraction(1, 15) and P_Ac_and_B == Fraction(1, 10):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')