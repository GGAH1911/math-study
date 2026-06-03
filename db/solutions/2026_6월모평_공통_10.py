import numpy as np
sqrt3 = np.sqrt(3)
a = 3 ** (sqrt3/6)
y_A = np.log(3) / np.log(a)
AB = np.sqrt((0-(-2))**2 + (y_A-0)**2)
AC = np.sqrt((0-2)**2 + (y_A-0)**2)
BC = np.sqrt((2-(-2))**2 + (0-0)**2)
if abs(AB - 4) < 1e-9 and abs(AC - 4) < 1e-9 and abs(BC - 4) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')