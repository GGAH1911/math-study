from fractions import Fraction
from itertools import permutations

cards = [Fraction(-3, 2), Fraction(-1, 2), Fraction(4, 3)]
max_val = float('-inf')
for perm in permutations(cards):
    a, b, c = perm
    val = 12 * (b - c) / a
    max_val = max(max_val, val)

if max_val == 68:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')