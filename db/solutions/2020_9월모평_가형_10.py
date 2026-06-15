from itertools import combinations
numbers = list(range(1, 8))
count_both_even = 0
total = 0
for selected in combinations(numbers, 3):
    total += 1
    remaining = [x for x in numbers if x not in selected]
    a = 1
    for x in selected:
        a *= x
    b = 1
    for x in remaining:
        b *= x
    if a % 2 == 0 and b % 2 == 0:
        count_both_even += 1
result = count_both_even / total
if abs(result - 6/7) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')