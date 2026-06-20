from itertools import product
from fractions import Fraction

# 공이 3인 경우: 주사위 3번의 합이 10
count_3 = 0
for roll in product(range(1, 7), repeat=3):
    if sum(roll) == 10:
        count_3 += 1

prob_3_case = Fraction(2, 5) * Fraction(count_3, 216)

# 공이 4인 경우: 주사위 4번의 합이 10
count_4 = 0
for roll in product(range(1, 7), repeat=4):
    if sum(roll) == 10:
        count_4 += 1

prob_4_case = Fraction(3, 5) * Fraction(count_4, 1296)

# 전체 확률
total_prob = prob_3_case + prob_4_case

if total_prob == Fraction(47, 540):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {total_prob}, expected 47/540')