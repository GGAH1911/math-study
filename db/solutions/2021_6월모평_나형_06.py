from fractions import Fraction

# 주어진 조건
P_A_union_B = 1
P_B = Fraction(1, 3)
P_A_inter_B = Fraction(1, 6)

# 덧셈 정리로 P(A) 구하기
# P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
P_A = P_A_union_B - P_B + P_A_inter_B
print(f'P(A) = {P_A}')

# 답: P(A^C)
P_A_complement = 1 - P_A
print(f'P(A^C) = {P_A_complement}')

# 검증
verify = P_A_union_B == P_A + P_B - P_A_inter_B
print(f'Verification check: {verify}')

if P_A_complement == Fraction(1, 6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')