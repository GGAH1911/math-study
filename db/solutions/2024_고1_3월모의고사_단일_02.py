x = 10
left = x/2 + 7
right = 2*x - 8
if abs(left - right) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')