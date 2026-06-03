from itertools import combinations
from fractions import Fraction

cards = list(range(1, 11))
all_combos = list(combinations(cards, 3))
total = len(all_combos)  # 120

favorable = [combo for combo in all_combos if min(combo) <= 4 or min(combo) >= 7]
count = len(favorable)  # 104

result = Fraction(count, total)
expected = Fraction(13, 15)

if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Got {result}, expected {expected}')
