from itertools import combinations
from fractions import Fraction

numbers = list(range(1, 11))
all_subsets = list(combinations(numbers, 3))

def product_even(s):
    p = 1
    for x in s: p *= x
    return p % 2 == 0

def sum_mult3(s):
    return sum(s) % 3 == 0

A = [s for s in all_subsets if product_even(s)]
AB = [s for s in A if sum_mult3(s)]

f = Fraction(len(AB), len(A))
if f == Fraction(19, 55):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')