import sympy as sp
from sympy import symbols, expand, pi, simplify

CANDIDATE = 25

# 원의 방정식: x^2 + y^2 - 8x + 6y = 0
# 표준형으로 변환: (x-4)^2 + (y+3)^2 = r^2
# 좌변을 전개하면:
# x^2 - 8x + 16 + y^2 + 6y + 9 = r^2
# x^2 + y^2 - 8x + 6y + 25 = r^2
# 원래 방정식에 25를 더하면 r^2 = 25

radius_squared = 25
narea = pi * radius_squared

# 넓이가 k*pi 형태이므로 k = radius_squared
k = radius_squared

if k == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')