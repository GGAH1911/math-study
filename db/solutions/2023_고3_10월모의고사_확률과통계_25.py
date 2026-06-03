from itertools import product

count = 0
for a, b, c, d in product(range(3), repeat=4):
    if a == 0:
        continue
    if a + b + c + d <= 7:
        count += 1

if count == 53:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')