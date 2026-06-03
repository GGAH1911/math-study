from itertools import permutations
from fractions import Fraction

valid_count = 0
total_count = 0

for perm in permutations([1, 2, 3, 4, 5]):
    f = {1: perm[0], 2: perm[1], 3: perm[2], 4: perm[3], 5: perm[4]}
    f_inv = {v: k for k, v in f.items()}
    total_count += 1
    cond_ga = (f[1] < f[3]) and (f[2] < f[4])
    cond_na = abs(f[1] - f[5]) >= f_inv[1]
    if cond_ga and cond_na:
        valid_count += 1

prob = Fraction(valid_count, total_count)
expected = Fraction(3, 20)
if prob == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob}, expected {expected}')