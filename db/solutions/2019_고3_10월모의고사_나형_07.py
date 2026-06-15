from itertools import product
count = 0
for x1, x2, x3 in product(range(1, 6), repeat=3):
    if x1 + x2 + x3 == 6:
        count += 1
print('VERIFY_PASS' if count == 10 else f'VERIFY_FAIL: got {count}')