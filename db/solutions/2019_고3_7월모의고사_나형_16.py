from itertools import permutations
count = 0
for a, b, c in permutations(range(1, 9), 3):
    if abs(a - b) > 1 and abs(b - c) > 1 and abs(a - c) > 1:
        count += 1
if count == 120:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')