from itertools import product
count = 0
for x in range(1, 11):
    for y in range(1, 11):
        for z in range(1, 11):
            for w in range(1, 11):
                if x + y + z + w == 11:
                    count += 1
from math import comb
expected = comb(10, 3)
print('VERIFY_PASS' if count == 120 and count == expected else 'VERIFY_FAIL')
