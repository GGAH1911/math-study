import math
import numpy as np

x = 6
left = math.log(x - 2) / math.log(3)
right = math.log(x + 10) / math.log(9)

if abs(left - right) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')