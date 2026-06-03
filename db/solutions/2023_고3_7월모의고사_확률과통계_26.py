from math import comb

# Case 1: 흰 공을 A에서 꺼냄 (확률 1/3)
prob_case1_draw = 1/3
prob_white_given_case1 = 1 - comb(3, 3) / comb(7, 3)

# Case 2: 검은 공을 A에서 꺼냄 (확률 2/3)
prob_case2_draw = 2/3
prob_white_given_case2 = 1 - comb(4, 3) / comb(7, 3)

# 전체 확률
total_prob = prob_case1_draw * prob_white_given_case1 + prob_case2_draw * prob_white_given_case2

# 분수로 변환 (32/35인지 확인)
from fractions import Fraction
result = Fraction(total_prob).limit_denominator(1000)
if result == Fraction(32, 35):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')