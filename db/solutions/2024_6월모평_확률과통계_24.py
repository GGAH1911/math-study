from fractions import Fraction

# 주어진 조건
P_A_and_Bc = Fraction(1, 9)  # P(A ∩ B^C)
P_Bc = Fraction(7, 18)        # P(B^C)

# 계산
P_B = 1 - P_Bc                # P(B)
P_A_union_B = P_A_and_Bc + P_B  # P(A ∪ B)

# 검증: P(A ∪ B) = P(A ∩ B^C) + P(B)가 맞는지 확인
# 이것은 P(A ∪ B) = P(A ∩ B^C) + P(A ∩ B) + P(A^C ∩ B)의 단순화
expected = Fraction(13, 18)

if P_A_union_B == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')