import math
BC = 9
sin_A = 3/5
AC = 9 / sin_A
if abs(AC - 15) < 1e-9 and abs(BC / AC - sin_A) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')