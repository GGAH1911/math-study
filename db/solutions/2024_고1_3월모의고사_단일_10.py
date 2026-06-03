import math
a = 6
sqrt3 = math.sqrt(3)
x1 = a + 3*sqrt3
x2 = a - 3*sqrt3
if x1 > 0 and x2 > 0 and abs((x1-a)**2 - 27) < 1e-10 and abs((x2-a)**2 - 27) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')