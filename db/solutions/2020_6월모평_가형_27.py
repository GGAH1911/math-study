CANDIDATE = 22
from itertools import permutations
from fractions import Fraction
from math import gcd

balls = (1, 1, 2, 2, 3, 3)
seen = set()
count_gt = 0
count_total = 0
for perm in permutations(balls):
    if perm in seen:
        continue
    seen.add(perm)
    count_total += 1
    m = perm[0]*100 + perm[1]*10 + perm[2]
    n = perm[3]*100 + perm[4]*10 + perm[5]
    if m > n:
        count_gt += 1

prob = Fraction(count_gt, count_total)  # q/p
q = prob.numerator
p = prob.denominator
result = p + q

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed p+q={result}, candidate={CANDIDATE}')
