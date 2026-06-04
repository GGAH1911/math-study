from itertools import combinations, permutations
from math import factorial

# 방법: 제2열의 3개 카드 합이 짝수인 경우
evens = [2, 4, 6, 8]
odds = [1, 3, 5, 7, 9]

# 합이 짝수인 경우
# Case 1: 3개 모두 짝수
case1 = len(list(combinations(evens, 3)))

# Case 2: 2개 홀수 + 1개 짝수
case2 = len(list(combinations(odds, 2))) * len(list(combinations(evens, 1)))

favor_choices = case1 + case2  # 44
favor_arrangements_in_col2 = factorial(3)  # 3! = 6
favor_arrangements_rest = factorial(6)  # 6!

favor_total = favor_choices * favor_arrangements_in_col2 * favor_arrangements_rest  # 190080
total_cases = factorial(9)  # 362880

prob_num = favor_total
prob_den = total_cases

# 기약분수로
from math import gcd
g = gcd(prob_num, prob_den)
prob_num //= g
prob_den //= g

if prob_num == 11 and prob_den == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')