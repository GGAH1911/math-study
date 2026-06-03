from math import comb

# 전체 경우의 수
total = comb(8, 5)
print(f'total cases: {total}')

# 조건을 만족하는 경우
# (1학년, 2학년, 3학년) = (1, 2, 2)
favorable = comb(1, 1) * comb(3, 2) * comb(4, 2)
print(f'favorable cases: {favorable}')

# 확률
prob_num = favorable
prob_den = total
print(f'probability: {prob_num}/{prob_den}')

# 기약분수로 약분
from math import gcd
g = gcd(prob_num, prob_den)
prob_num //= g
prob_den //= g
print(f'simplified: {prob_num}/{prob_den}')

# 답 검증: 9/28
if prob_num == 9 and prob_den == 28:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')