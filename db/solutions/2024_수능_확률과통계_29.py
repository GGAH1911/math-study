import itertools
count = 0
for a in range(1, 7):
    for b in range(1, 7):
        for c in range(1, 7):
            for d in range(1, 7):
                if a <= c <= d and b <= c <= d:
                    count += 1
if count == 196:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')