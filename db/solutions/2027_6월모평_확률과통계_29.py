from itertools import product
from math import gcd

# 5개 주사위 모두 홀수인 경우
odd_faces = [1, 3, 5]
count_sum_15 = 0
total_odd = 0

for dice in product(odd_faces, repeat=5):
    total_odd += 1
    if sum(dice) == 15:
        count_sum_15 += 1

# P(곱이 홀수) = (1/2)^5
prob_odd_product = 1/32

# P(합=15 and 곱이 홀수) = count_sum_15 / 6^5
prob_sum_15_and_odd = count_sum_15 / (6**5)

# 조건부 확률
conditional_prob = prob_sum_15_and_odd / prob_odd_product

# 분자, 분모 구하기
numerator = count_sum_15 * 32
denominator = 6**5

# 기약분수로 정리
common = gcd(numerator, denominator)
q = numerator // common
p = denominator // common

# 검증
if q/p == conditional_prob and gcd(p, q) == 1:
    answer = p + q
    if answer == 98:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')