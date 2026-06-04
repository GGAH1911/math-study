import math
from sympy import *

# 주어진 조건
AB = 4
BC = 8
cos_A = Rational(-1, 4)
AC = 6

# 코사인 법칙으로 검증
# BC^2 = AB^2 + AC^2 - 2*AB*AC*cos(A)
lhs = BC**2
rhs = AB**2 + AC**2 - 2*AB*AC*cos_A

if lhs == rhs:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')