import math
a = 2
x1, y1 = 2, math.log(2, 4)
x2, y2 = 4, math.log(a, 2)
x0, y0 = 0, 0
m1 = y1 / x1
m2 = y2 / x2
m0 = (y1 - y0) / (x1 - x0) if x1 != x0 else float('inf')
m0_check = (y2 - y0) / (x2 - x0) if x2 != x0 else float('inf')
if abs(m0 - m0_check) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')