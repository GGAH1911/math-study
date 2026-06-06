count = 0
for a in range(1, 6):
    for b in range(1, 6):
        for c in range(1, 6):
            for d in range(1, 6):
                if a <= b+1 and b+1 <= c and c <= d:
                    count += 1
if count == 55:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')