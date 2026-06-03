count = 0
for a in range(11):
    for b in range(11 - a):
        for c in range(11 - a - b):
            for d in range(11 - a - b - c):
                e = 10 - a - b - c - d
                if e >= 0 and abs(a - b + c - d + e) <= 2:
                    count += 1
if count == 371:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')