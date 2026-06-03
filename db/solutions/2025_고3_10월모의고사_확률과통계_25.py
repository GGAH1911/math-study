from itertools import product

count = 0
for a, b in product(range(1, 7), repeat=2):
    if abs(a - b) == 1:
        count += 1

total = 36
probability = count / total
expected = 5 / 18

if abs(probability - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')