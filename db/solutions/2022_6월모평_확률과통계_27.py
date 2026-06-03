from math import comb
from fractions import Fraction

# 주사위 2개의 모든 경우
dice_cases = [(a, b) for a in range(1, 7) for b in range(1, 7)]

# 동전 4개에서 앞면이 k개 나올 때, 주사위 곱이 k인 경우를 찾기
total_prob = Fraction(0)

for k in range(5):
    # 주사위 곱이 k인 경우의 수
    matching_dice_count = sum(1 for a, b in dice_cases if a * b == k)
    # 동전에서 앞면 k개
    coin_ways = comb(4, k)
    # 이 k에 대한 확률 기여
    contribution = Fraction(matching_dice_count, 36) * Fraction(coin_ways, 16)
    total_prob += contribution

expected = Fraction(3, 64)

if total_prob == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: {expected}, Got: {total_prob}')