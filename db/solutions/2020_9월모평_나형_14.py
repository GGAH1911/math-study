import itertools
from fractions import Fraction

points = [(a, b) for a in range(1, 5) for b in range(1, 4)]
all_pairs = list(itertools.combinations(points, 2))

count_greater_than_1 = 0
for p1, p2 in all_pairs:
    distance_squared = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
    if distance_squared > 1:
        count_greater_than_1 += 1

result = Fraction(count_greater_than_1, len(all_pairs))
expected = Fraction(49, 66)

if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')