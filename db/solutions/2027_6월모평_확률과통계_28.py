from itertools import product
from math import gcd

initial = [0, 1, 1, 1, 1, 0]
target  = [1, 1, 1, 1, 1, 1]

def simulate(seq, state):
    s = list(state)
    for k in seq:
        if k % 2 == 1:
            for c in range(1, k+1):
                s[c-1] ^= 1
        else:
            for c in range(k, 7):
                s[c-1] ^= 1
    return s

count = sum(1 for seq in product(range(1,7), repeat=4)
            if simulate(seq, initial) == target)
total = 6**4
g = gcd(count, total)
assert count == 160 and total == 1296
if count * 81 == total * 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')