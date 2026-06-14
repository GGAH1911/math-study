from itertools import product

def get_affected(dice):
    mapping = {1: {6,1,2}, 2: {1,2,3}, 3: {2,3,4}, 4: {3,4,5}, 5: {4,5,6}, 6: {5,6,1}}
    return mapping[dice]

count = 0
for a, b, c in product(range(1, 7), repeat=3):
    affected = get_affected(a) | get_affected(b) | get_affected(c)
    if affected == {1, 2, 3, 4, 5, 6}:
        count += 1

from math import gcd
total = 216
g = gcd(count, total)
result_num, result_den = count // g, total // g

if result_num == 17 and result_den == 36:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')