from fractions import Fraction

# 주어진 조건
P_A_complement = Fraction(3, 4)
P_A_union_B = Fraction(5, 6)

# 계산한 값
P_A = 1 - P_A_complement
P_B = Fraction(7, 12)

# 배반사건이므로 P(A∪B) = P(A) + P(B)
verify_union = P_A + P_B
verify_A_complement = 1 - P_A

# 검증
if verify_union == P_A_union_B and verify_A_complement == P_A_complement:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')