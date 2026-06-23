from itertools import product

count = 0
for a in range(1, 9):
    for b in range(1, 9):
        for c in range(1, 9):
            d = 8 - a - b - c
            if d >= 1 and a > b:
                count += 1

if count == 13:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')