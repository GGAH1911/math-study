from itertools import permutations
from fractions import Fraction

X = {1, 2, 3, 4}
Y = {1, 2, 3, 4, 5, 6, 7}

total_count = 0
satisfy_count = 0

for perm in permutations(Y, 4):
    f = {1: perm[0], 2: perm[1], 3: perm[2], 4: perm[3]}
    total_count += 1
    
    if f[2] == 2:
        product = f[1] * f[2] * f[3] * f[4]
        if product % 4 == 0:
            satisfy_count += 1

prob = Fraction(satisfy_count, total_count)
if prob == Fraction(4, 35):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')