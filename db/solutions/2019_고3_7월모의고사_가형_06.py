from fractions import Fraction

# 주사위: 1~6
dice = [1, 2, 3, 4, 5, 6]
odd_count = sum(1 for x in dice if x % 2 == 1)
total = len(dice)

# 5번 모두 홀수가 나올 확률
prob_all_odd = (Fraction(odd_count, total)) ** 5
print(f'P(all odd) = {prob_all_odd}')

# 곱이 짝수일 확률
prob_product_even = 1 - prob_all_odd
print(f'P(product even) = {prob_product_even}')

# 답 검증
if prob_product_even == Fraction(31, 32):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')