from itertools import product
from fractions import Fraction

# 모든 경우의 수
all_outcomes = list(product(range(1, 7), repeat=2))
total = len(all_outcomes)

# 조건을 만족하는 경우
valid_count = 0
for a, b in all_outcomes:
    if (a + b == 7) or (a * b % 6 == 0):
        valid_count += 1

probability = Fraction(valid_count, total)
print(f'유효한 경우의 수: {valid_count}, 전체: {total}')
print(f'확률: {probability}')
if probability == Fraction(17, 36):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')