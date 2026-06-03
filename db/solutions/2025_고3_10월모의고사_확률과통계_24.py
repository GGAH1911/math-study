from fractions import Fraction

P_A = Fraction(1, 4)
P_B = Fraction(1, 12)

# 조건 1: P(A ∪ B) = 1/3 (배반사건이므로)
P_A_union_B = P_A + P_B
assert P_A_union_B == Fraction(1, 3), f"P(A∪B) = {P_A_union_B}, expected 1/3"

# 조건 2: P(A^c) = P(A) + 1/2
P_A_complement = 1 - P_A
expected = P_A + Fraction(1, 2)
assert P_A_complement == expected, f"P(A^c) = {P_A_complement}, P(A) + 1/2 = {expected}"

print('VERIFY_PASS')