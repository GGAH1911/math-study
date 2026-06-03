result = 2**(-1) * 8**(5/3)
expected = 16
if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')