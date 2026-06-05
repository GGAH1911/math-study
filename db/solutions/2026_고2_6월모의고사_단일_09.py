import math
a = 2
b = 2**a
dist = abs(b - (-3))
if dist == 7 and b == 2**a:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')