from fractions import Fraction

# 주어진 조건
P_B_given_A = Fraction(1, 4)
P_A_given_B = Fraction(1, 3)
P_A_plus_P_B = Fraction(7, 10)

# 답
P_A_and_B = Fraction(1, 10)

# 검증: 조건부 확률 정의로부터 P(A), P(B) 역산
# P(B|A) = P(A∩B) / P(A) = 1/4 => P(A) = 4·P(A∩B)
P_A_candidate = P_A_and_B * 4

# P(A|B) = P(A∩B) / P(B) = 1/3 => P(B) = 3·P(A∩B)
P_B_candidate = P_A_and_B * 3

# 조건 검증
check1 = (P_A_and_B / P_A_candidate == P_B_given_A)
check2 = (P_A_and_B / P_B_candidate == P_A_given_B)
check3 = (P_A_candidate + P_B_candidate == P_A_plus_P_B)

if check1 and check2 and check3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')