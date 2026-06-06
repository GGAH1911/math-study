count = 0
for a in range(1, 9):
    for b in range(a, 9):
        for c in range(b, 9):
            if (a - b) * (b - c) == 0:
                count += 1
if count == 64:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')