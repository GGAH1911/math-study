i = 1j
result = 1 + 2 / (1 - i)
expected = 2 + i
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')