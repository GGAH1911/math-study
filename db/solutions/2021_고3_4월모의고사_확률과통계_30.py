from itertools import product

count = 0
for x1 in range(1, 15):
    for x2 in range(1, 15):
        for x3 in range(1, 15):
            for x4 in range(1, 15):
                if x1 + x2 + x3 + x4 == 34:
                    if x1 % 2 == 1 and x3 % 2 == 1 and x2 % 2 == 0 and x4 % 2 == 0:
                        count += 1

if count == 206:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')