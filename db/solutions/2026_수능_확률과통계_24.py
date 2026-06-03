from fractions import Fraction

P_A = Fraction(2, 5)
P_B_given_A = Fraction(1, 4)
P_A_intersect_B = P_B_given_A * P_A

P_B = Fraction(7, 10)
P_A_union_B = P_A + P_B - P_A_intersect_B

assert P_A_intersect_B == Fraction(1, 10), f"Expected 1/10, got {P_A_intersect_B}"
assert P_A_union_B == 1, f"Expected P(A∪B)=1, got {P_A_union_B}"
assert P_B == Fraction(7, 10), f"Expected 7/10, got {P_B}"

print('VERIFY_PASS')