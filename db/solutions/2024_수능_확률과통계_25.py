from math import factorial

# 전체 경우의 수
total = factorial(6)

# 조건 위반: 양 끝이 (5,6) 또는 (6,5)
bad_cases = 0
for left in [1,2,3,4,5,6]:
    for right in [1,2,3,4,5,6]:
        if left != right:
            if left + right > 10:
                remaining = [x for x in [1,2,3,4,5,6] if x != left and x != right]
                bad_cases += factorial(len(remaining))

good_cases = total - bad_cases
prob_num = good_cases
prob_den = total

# 기약분수로 정리
from math import gcd
g = gcd(prob_num, prob_den)
prob_num //= g
prob_den //= g

if prob_num == 14 and prob_den == 15:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {prob_num}/{prob_den}')