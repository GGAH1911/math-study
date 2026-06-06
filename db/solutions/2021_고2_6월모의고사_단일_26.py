import numpy as np
from scipy.optimize import fsolve

m = 3

def f(x):
    return 2**x + m

point_check = f(1)
if abs(point_check - 5) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')