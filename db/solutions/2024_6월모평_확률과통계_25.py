from math import comb

# 전체 경우의 수
total = comb(9, 4)
print(f'Total cases: {total}')

# 빨강 2장 이상인 경우의 수
red_2 = comb(4, 2) * comb(5, 2)
red_3 = comb(4, 3) * comb(5, 1)
red_4 = comb(4, 4) * comb(5, 0)

favorable = red_2 + red_3 + red_4
print(f'Red 2: {red_2}, Red 3: {red_3}, Red 4: {red_4}')
print(f'Favorable cases: {favorable}')

# 확률
prob_num = favorable
prob_den = total

# 최대공약수로 기약분수화
from math import gcd
g = gcd(prob_num, prob_den)
prob_num //= g
prob_den //= g

print(f'Probability: {prob_num}/{prob_den}')

# 검증: 9/14
if prob_num == 9 and prob_den == 14:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')