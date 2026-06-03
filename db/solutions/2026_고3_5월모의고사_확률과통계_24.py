from fractions import Fraction

P_AunionB = Fraction(5, 8)
P_A = Fraction(3, 8)

# 배반사건: P(A ∩ B) = 0
P_B = P_AunionB - P_A
assert P_B == Fraction(1, 4), f'P(B) should be 1/4, got {P_B}'

# 배반사건 검증: P(A) + P(B) = P(A ∪ B)
assert P_A + P_B == P_AunionB, 'Union formula violated'

# B^C (B의 여사건)
P_Bc = 1 - P_B
assert P_Bc == Fraction(3, 4), f'P(B^C) should be 3/4, got {P_Bc}'

print('VERIFY_PASS')