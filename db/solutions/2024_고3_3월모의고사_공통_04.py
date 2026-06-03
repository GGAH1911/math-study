import sympy as sp

a = -2

# 좌극한 (x < 3 구간)
left_limit = 2*3 + a  # = 4

# f(3) (x >= 3 구간)
import math
f3 = math.sqrt(3 + 1) - a  # = 2 - (-2) = 4

if abs(left_limit - f3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
