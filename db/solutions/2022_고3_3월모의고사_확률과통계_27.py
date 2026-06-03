count = 0
for x1 in range(0, 6):
    for x2 in range(0, 6):
        for x3 in range(0, 9):
            if x1 + x2 + x3 == 8:
                count += 1
print('VERIFY_PASS' if count == 33 else 'VERIFY_FAIL')