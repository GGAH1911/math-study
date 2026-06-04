import math
k = 5/4
f_k = (2**(k+k)) - math.sqrt(2)
expected = 3*math.sqrt(2)
if abs(f_k - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')