from itertools import product
from fractions import Fraction

X = [1, 2, 3, 4]

def divides(a, b):
    return b % a == 0

def satisfies_condition(f):
    for a in X:
        for b in X:
            if divides(a, b):
                if not divides(f[a], f[b]):
                    return False
    return True

total = 0
f4_even = 0

for vals in product(X, repeat=4):
    f = {1: vals[0], 2: vals[1], 3: vals[2], 4: vals[3]}
    if satisfies_condition(f):
        total += 1
        if f[4] % 2 == 0:
            f4_even += 1

prob = Fraction(f4_even, total)
expected = Fraction(27, 40)

if prob == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Got {prob}, expected {expected}')
    print(f'total={total}, f4_even={f4_even}')
