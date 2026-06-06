p = (2 + 2 + 0) / 3
q = (0 + 6 + 3) / 3
result = p * q
if abs(result - 4) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')