from math import comb
result = comb(7, 5)
expected = 21
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')