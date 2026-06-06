sum1 = sum((k+1)**2 for k in range(1, 7))
sum2 = sum((k-1)**2 for k in range(1, 6))
result = sum1 - sum2
expected = 109
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')