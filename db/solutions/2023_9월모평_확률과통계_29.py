from itertools import product
from math import gcd

count_sum_11 = 0
for draws in product(range(1, 7), repeat=4):
    if sum(draws) == 11:
        count_sum_11 += 1

total = 6**4
prob_num = count_sum_11
prob_den = total

g = gcd(prob_num, prob_den)
q = prob_num // g
p = prob_den // g

answer = p + q
expected = 175

if answer == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {answer}, expected {expected}')