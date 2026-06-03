from fractions import Fraction

# 주어진 조건
P_union = Fraction(5, 6)
P_Ac_and_B = Fraction(1, 4)

# 유도된 답
P_A = Fraction(7, 12)
P_Ac = Fraction(5, 12)

# 검증: P(A^c ∩ B) = P(B) - P(A ∩ B)
# P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
# P(A^c ∩ B) = P(B) - P(A ∩ B) = 1/4

# P(A) + P(B) - P(A ∩ B) = 5/6
# P(B) - P(A ∩ B) = 1/4 이므로
# P(A) + 1/4 = 5/6
# P(A) = 5/6 - 1/4 = 7/12

if P_A == Fraction(7, 12) and P_Ac == 1 - P_A:
    # 검증: P(A ∪ B)와 주어진 조건으로부터 B와 A∩B의 값 확인
    # P(B) - P(A∩B) = 1/4에서 P(B)와 P(A∩B)는 여러 값 가능하나
    # P(A) + [P(B) - P(A∩B)] = 7/12 + 1/4 = 7/12 + 3/12 = 10/12 = 5/6 ✓
    if P_A + P_Ac_and_B == P_union:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')