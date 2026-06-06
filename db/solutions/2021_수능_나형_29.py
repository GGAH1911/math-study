from math import comb

# 경우 1: 공 3을 꺼낸 경우, 주사위 3번 던져 합이 10
# a' + b' + c' = 7 (0 <= a', b', c' <= 5)
count_3dice = comb(9, 2) - 3 * comb(3, 2)
prob_3dice = count_3dice / (6**3)
prob_case1 = (2/5) * prob_3dice

# 경우 2: 공 4를 꺼낸 경우, 주사위 4번 던져 합이 10
# a' + b' + c' + d' = 6 (0 <= a', b', c', d' <= 5)
count_4dice = comb(9, 3) - 4 * comb(3, 3)
prob_4dice = count_4dice / (6**4)
prob_case2 = (3/5) * prob_4dice

# 전체 확률
total_prob = prob_case1 + prob_case2

# 분수로 표현
from fractions import Fraction
frac = Fraction(total_prob).limit_denominator(10000)

q, p = frac.numerator, frac.denominator

if p == 540 and q == 47:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {q}/{p}')