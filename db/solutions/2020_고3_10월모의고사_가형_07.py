from fractions import Fraction
from sympy import Eq, symbols, solve

CANDIDATE = Fraction(3, 5)

# 주머니 A: 흰 공 21, 검은 공 29 (총 50)
# 주머니 B: 흰 공 14, 검은 공 36 (총 50)

# P(A) = P(B) = 1/2
prob_choose_A = Fraction(1, 2)
prob_choose_B = Fraction(1, 2)

# P(흰 공 | A) = 21/50
prob_white_given_A = Fraction(21, 50)

# P(흰 공 | B) = 14/50
prob_white_given_B = Fraction(14, 50)

# 전체 확률: P(흰 공) = P(흰 공|A)P(A) + P(흰 공|B)P(B)
prob_white = prob_white_given_A * prob_choose_A + prob_white_given_B * prob_choose_B

# 조건부 확률: P(A | 흰 공) = P(흰 공|A) * P(A) / P(흰 공)
prob_A_given_white = (prob_white_given_A * prob_choose_A) / prob_white

if prob_A_given_white == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')