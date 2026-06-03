count = 0
for a in range(1, 7):
    for b in range(1, 7):
        if a**2 + b <= 6:
            count += 1
if count == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')