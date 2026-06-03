from fractions import Fraction

# 주어진 조건
P_A_union_B = Fraction(9, 10)
P_A = Fraction(2, 5)

# 배반사건이므로 P(A ∪ B) = P(A) + P(B)
P_B = P_A_union_B - P_A

# 검증: P(A ∪ B) = P(A) + P(B)
verify = P_A + P_B

if verify == P_A_union_B:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')