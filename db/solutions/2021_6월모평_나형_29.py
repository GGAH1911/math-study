from itertools import product

count = 0
for f1 in range(1, 5):
    for f2 in range(1, 5):
        if f1 * f2 < 9:
            continue
        for f3 in range(1, 5):
            for f4 in range(1, 5):
                image = set([f1, f2, f3, f4])
                if len(image) == 3:
                    count += 1

if count == 32:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected 32, got {count}')