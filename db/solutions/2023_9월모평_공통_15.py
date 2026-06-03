import numpy as np
from fractions import Fraction

# Given values
a1 = -14
r = Fraction(-1, 2)

# Generate sequence
a = [None] * 101  # a[0] unused, a[1] to a[100]
a[1] = a1

for n in range(1, 100):
    if abs(a[n]) < 5:
        a[n+1] = a[n] + 3
    else:
        a[n+1] = -Fraction(1, 2) * a[n]

# Verify condition (가): a_{4k} = r^k
for k in range(1, 26):
    expected = r ** k
    if a[4*k] != expected:
        print('VERIFY_FAIL')
        exit()

# Count m where |a_m| >= 5 for m <= 100
count = 0
for m in range(1, 101):
    if abs(a[m]) >= 5:
        count += 1

p = count
result = p + a1

if result == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')