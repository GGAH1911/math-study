import math
from numpy import sqrt

# 포물선 정의: 꼭짓점 (1,0), 준선 x=-1
# 표준형: y^2 = 8(x-1)

# 점 (3, a) 대입
x, a = 3, 4

# 포물선 방정식 만족 확인
lhs = a**2
rhs = 8 * (x - 1)

if abs(lhs - rhs) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')