count = 0
for a in range(-49, 50):
    if -50 < a < 50 and a % 7 != 0:
        count += 1
if count == 84:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')