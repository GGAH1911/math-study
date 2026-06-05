from math import comb
n, r = 3, 6
result = comb(n + r - 1, r)
expected = 28
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')