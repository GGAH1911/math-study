from itertools import product
from math import gcd

B = [1, 2, 3]
count_satisfied = 0

for f_values in product(B, repeat=4):
    f_1, f_2, f_3, f_4 = f_values
    cond1 = f_1 >= 2
    cond2 = set(f_values) == {1, 2, 3}
    if cond1 or cond2:
        count_satisfied += 1

total = 81
g = gcd(count_satisfied, total)
numerator = count_satisfied // g
denominator = total // g

if numerator == 22 and denominator == 27:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')