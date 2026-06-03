from math import comb

# 전체 경우의 수
total = comb(14, 3)
print(f'Total cases: {total}')

# 모두 검은색인 경우
all_black = comb(9, 3)
print(f'All black cases: {all_black}')

# 적어도 한 개가 흰색일 확률
at_least_one_white = 1 - (all_black / total)
print(f'P(at least one white) = {at_least_one_white}')

# 기약분수로 표현
from fractions import Fraction
result = Fraction(total - all_black, total)
print(f'Simplified: {result}')

if result == Fraction(10, 13):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')