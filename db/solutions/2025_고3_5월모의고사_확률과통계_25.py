from itertools import product

total = 0
favorable = 0
for a, b, c in product(range(1, 7), repeat=3):
    total += 1
    if (a * b * c) % 3 == 0:
        favorable += 1

from fractions import Fraction
prob = Fraction(favorable, total)
expected = Fraction(19, 27)
if prob == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob}, expected {expected}')
