from itertools import product
count = 0
for a, b, c in product(range(1, 7), repeat=3):
    if a > b and a > c:
        count += 1
candidate = 55 / 216
actual_prob = count / 216
if abs(actual_prob - candidate) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')