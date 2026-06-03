import math
from sympy import *

# 답: 7/2 * log_2(3) - 7/4
a = log(3, 2)
area = 7*a/2 - 7/4

# 조건 검증: AB = 2*CD
# A = (log_2(3), 2/3), B = (log_2(3), 3)
AB = 3 - 2/3  # = 7/3

# C = (1 - log_2(3), 2/3), D = (1 - log_2(3), -1/2)
CD = 2/3 - (-1/2)  # = 7/6

if abs(AB - 2*CD) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')