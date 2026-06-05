count = 0
for x in range(1, 1000):
    if 2**(13 - 2*x) >= 8:
        count += 1
print('VERIFY_PASS' if count == 5 else 'VERIFY_FAIL')