from fractions import Fraction

# Given conditions
P_A_intersect_B = Fraction(1, 5)
P_A_plus_P_B = Fraction(7, 10)

# From A and B^c being disjoint: A ⊆ B, so P(A ∩ B) = P(A)
P_A = P_A_intersect_B  # = 1/5

# From P(A) + P(B) = 7/10
P_B = P_A_plus_P_B - P_A  # = 7/10 - 1/5 = 1/2

# Verify: A ⊆ B means P(A^c ∩ B) = P(B) - P(A ∩ B) = P(B) - P(A)
P_A_complement_intersect_B = P_B - P_A

# Check if answer is 3/10
answer = Fraction(3, 10)
if P_A_complement_intersect_B == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')