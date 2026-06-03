from fractions import Fraction

P_A = Fraction(1, 2)
P_A_cap_Bc = Fraction(2, 7)

P_A_cap_B = P_A - P_A_cap_Bc
P_B_answer = Fraction(3, 14)

if P_A_cap_B == P_B_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')