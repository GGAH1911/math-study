from itertools import product
count = 0
for seq in product('abc', repeat=5):
    if 'a' in seq and 'b' in seq and 'c' in seq:
        count += 1
print('VERIFY_PASS' if count == 150 else f'VERIFY_FAIL: {count}')