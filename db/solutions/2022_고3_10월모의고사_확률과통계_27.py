from itertools import combinations
from fractions import Fraction

total = 0
favorable = 0

for combo in combinations(range(1, 11), 4):
    a1, a2, a3, a4 = sorted(combo)
    total += 1
    if (a1 * a2) % 2 == 1 and (a3 + a4) >= 16:
        favorable += 1

prob = Fraction(favorable, total)
expected = Fraction(9, 70)

if prob == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob}, expected {expected}')
