from fractions import Fraction

# 주어진 조건
P_A_complement = Fraction(5, 6)
P_A_union_B = Fraction(3, 4)

# P(A) 계산
P_A = 1 - P_A_complement
assert P_A == Fraction(1, 6), f'P(A) should be 1/6, got {P_A}'

# 배반사건이므로 P(A ∪ B) = P(A) + P(B)
P_B = P_A_union_B - P_A
assert P_B == Fraction(7, 12), f'P(B) should be 7/12, got {P_B}'

# P(B^C) 계산
P_B_complement = 1 - P_B
assert P_B_complement == Fraction(5, 12), f'P(B^C) should be 5/12, got {P_B_complement}'

# 원래 조건 검증
assert P_A_complement == Fraction(5, 6), f'P(A^C) verification failed'
assert P_A + P_B == P_A_union_B, f'P(A ∪ B) verification failed'

print('VERIFY_PASS')