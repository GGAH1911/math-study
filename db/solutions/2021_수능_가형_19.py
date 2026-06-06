from itertools import product
from fractions import Fraction

# 주사위 3번 합이 10인 경우
count_3dice_10 = 0
for rolls in product(range(1, 7), repeat=3):
    if sum(rolls) == 10:
        count_3dice_10 += 1

# 주사위 4번 합이 10인 경우
count_4dice_10 = 0
for rolls in product(range(1, 7), repeat=4):
    if sum(rolls) == 10:
        count_4dice_10 += 1

# 확률 계산
prob_3dice = Fraction(count_3dice_10, 216)
prob_4dice = Fraction(count_4dice_10, 1296)

prob_ball_3 = Fraction(2, 5)
prob_ball_4 = Fraction(3, 5)

total_prob = prob_ball_3 * prob_3dice + prob_ball_4 * prob_4dice

if total_prob == Fraction(47, 540):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')