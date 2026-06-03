from itertools import permutations
from fractions import Fraction

digits = [1, 2, 3, 4, 5]

all_numbers = set()
for perm in permutations(digits, 4):
    num = perm[0]*1000 + perm[1]*100 + perm[2]*10 + perm[3]
    all_numbers.add(num)

total = len(all_numbers)  # should be 120
A = {n for n in all_numbers if n % 5 == 0}
B = {n for n in all_numbers if n >= 3500}
AuB = A | B

prob_frac = Fraction(len(AuB), total)
expected = Fraction(3, 5)

if prob_frac == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob_frac}, expected {expected}, |A|={len(A)}, |B|={len(B)}, |AuB|={len(AuB)}, total={total}')
