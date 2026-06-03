from itertools import product

count = 0
for x in range(1, 12):
    for y in range(1, 12):
        for z in range(1, 12):
            for w in range(1, 12):
                if 3*x + y + z + w == 11:
                    count += 1

if count == 27:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')