from fractions import Fraction
P_A = Fraction(1, 12)
P_A_union_B = Fraction(11, 12)
P_B = Fraction(5, 6)
P_A_intersect_B = Fraction(0, 1)
computed = P_A + P_B - P_A_intersect_B
if computed == P_A_union_B:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')