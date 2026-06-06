import math
from sympy import *
x_val = 7
lhs = math.log(x_val - 3, 2)
rhs = math.log(3*x_val - 5, 4)
if abs(lhs - rhs) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')