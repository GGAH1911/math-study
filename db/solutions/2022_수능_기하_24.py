import math
from sympy import sqrt, symbols

# 주어진 조건
a_squared = 12
b_squared = 6
focus_x = 3 * sqrt(2)

# 쌍곡선 c^2 = a^2 + b^2 검증
c_squared = a_squared + b_squared
c = sqrt(c_squared)

# 초점 좌표 (3√2, 0) 검증
if c == focus_x:
    major_axis_length = 2 * sqrt(a_squared)
    if major_axis_length == 4 * sqrt(3):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')