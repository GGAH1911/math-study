from itertools import product
count = 0
for f1 in range(1, 5):
    for f2 in range(1, 5):
        for f3 in range(1, 5):
            for f4 in range(1, 5):
                if f2 <= f3 <= f4:
                    count += 1
if count == 80:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')