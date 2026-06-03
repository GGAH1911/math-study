import itertools
from fractions import Fraction

cards = [1, 2, 3, 4, 5, 6, 7]
all_perms = list(itertools.permutations(cards))
total_count = len(all_perms)

even_product_count = 0
for perm in all_perms:
    product = perm[0] * perm[-1]
    if product % 2 == 0:
        even_product_count += 1

probability = Fraction(even_product_count, total_count)
expected = Fraction(5, 7)

if probability == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')