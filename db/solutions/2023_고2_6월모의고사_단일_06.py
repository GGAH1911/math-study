import math
AB = 3
AC = 6
cos_A = 5/9
BC = 5

BC_squared = AB**2 + AC**2 - 2*AB*AC*cos_A
if abs(BC_squared - BC**2) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')