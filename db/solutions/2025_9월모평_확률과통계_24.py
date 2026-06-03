from fractions import Fraction

# 주어진 조건
P_A = Fraction(2, 3)
P_A_and_B = Fraction(1, 6)

# 독립성으로부터 P(B) 계산
P_B = P_A_and_B / P_A

# 합집합 확률
P_A_or_B = P_A + P_B - P_A_and_B

# 검증
if P_A_or_B == Fraction(3, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')