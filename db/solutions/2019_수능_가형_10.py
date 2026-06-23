from math import gcd
from itertools import combinations

numbers = list(range(2, 9))  # [2,3,4,5,6,7,8]
all_pairs = list(combinations(numbers, 2))
total = len(all_pairs)  # 21

coprime_pairs = [(a, b) for a, b in all_pairs if gcd(a, b) == 1]
coprime_count = len(coprime_pairs)

from fractions import Fraction
prob = Fraction(coprime_count, total)

expected = Fraction(2, 3)
if prob == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob}, expected {expected}')
