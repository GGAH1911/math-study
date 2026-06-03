import math
a2 = 16
b2 = 7
c2 = a2 - b2
c = math.sqrt(c2)
dist_foci = 2 * c
if abs(dist_foci - 6) < 1e-9 and 0 < math.sqrt(b2) < 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')