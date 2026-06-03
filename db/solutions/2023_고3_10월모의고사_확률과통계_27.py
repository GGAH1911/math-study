from itertools import permutations
from math import gcd

count = 0
remaining = [2, 3, 4, 5, 6, 7, 8]
for perm in permutations(remaining):
    circle = [1] + list(perm)
    valid = all(gcd(circle[i], circle[(i+1) % 8]) == 1 for i in range(8))
    if valid:
        count += 1

if count == 72:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')
