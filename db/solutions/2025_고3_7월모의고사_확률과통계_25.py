from itertools import combinations
numbers = list(range(1, 13))
divisors_of_8 = [1, 2, 4, 8]
total_pairs = list(combinations(numbers, 2))
count_at_least_one_divisor = sum(1 for a, b in total_pairs if a in divisors_of_8 or b in divisors_of_8)
prob_num = count_at_least_one_divisor
prob_den = len(total_pairs)
from math import gcd
g = gcd(prob_num, prob_den)
prob_num //= g
prob_den //= g
if prob_num == 19 and prob_den == 33:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')