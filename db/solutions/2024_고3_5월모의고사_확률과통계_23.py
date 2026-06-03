from fractions import Fraction

# 주어진 조건
P_union = Fraction(2, 3)

# 우리의 답
P_intersection = Fraction(2, 9)

# 두 번째 조건으로부터 P(A) + P(B)를 구함
P_A_plus_B = 4 * P_intersection

# 덧셈 공식으로 P(A ∪ B) 검증
P_union_check = P_A_plus_B - P_intersection

if P_union_check == P_union:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')