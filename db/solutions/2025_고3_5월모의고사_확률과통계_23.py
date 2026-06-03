from fractions import Fraction

P_A = Fraction(1, 4)
P_B = Fraction(1, 6)
P_A_intersect_B = Fraction(0)  # 배반사건

P_A_union_B = P_A + P_B - P_A_intersect_B

expected_answer = Fraction(5, 12)

if P_A_union_B == expected_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')