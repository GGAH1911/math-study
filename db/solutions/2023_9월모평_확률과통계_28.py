from itertools import combinations
from math import gcd

count = 0
total = 0

for combo in combinations(range(1, 11), 3):
    total += 1
    a, b, c = combo
    product = a * b * c
    s = a + b + c
    if product % 5 == 0 and s % 3 == 0:
        count += 1

g = gcd(count, total)
numerator = count // g
denominator = total // g

if numerator == 11 and denominator == 60:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {numerator}/{denominator}, expected 11/60')
