from itertools import combinations

# 1부터 11까지
numbers = list(range(1, 12))

# 7 이상의 홀수
odd_seven_or_more = {7, 9, 11}

# 모든 2개 조합
all_pairs = list(combinations(numbers, 2))
total = len(all_pairs)

# 적어도 하나가 7 이상의 홀수인 경우
count_at_least_one = sum(1 for pair in all_pairs if pair[0] in odd_seven_or_more or pair[1] in odd_seven_or_more)

# 확률
from fractions import Fraction
prob = Fraction(count_at_least_one, total)

if prob == Fraction(27, 55):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')