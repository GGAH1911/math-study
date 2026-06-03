import math
from fractions import Fraction

# 전체 경우의 수
total = 6**4

# 곱이 27의 배수가 되는 경우
count = 0
for a in range(1, 7):
    for b in range(1, 7):
        for c in range(1, 7):
            for d in range(1, 7):
                product = a * b * c * d
                if product % 27 == 0:
                    count += 1

prob = Fraction(count, total)
print(f'경우의 수: {count}/{total}')
print(f'확률: {prob}')
if prob == Fraction(1, 9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')