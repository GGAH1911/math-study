import sympy as sp
from sympy import sqrt

# 포물선: y^2 = 8x
# P의 x좌표 = 3 (y축으로부터 거리 3)
p_x = 3

# P는 포물선 위에 있으므로
p_y_squared = 8 * p_x  # = 24
p_y = sqrt(p_y_squared)  # = 2*sqrt(6)

# 초점 F(2, 0)
F_x, F_y = 2, 0

# PF의 길이
PF = sqrt((p_x - F_x)**2 + (p_y - F_y)**2)
PF_simplified = sp.simplify(PF)

# 검증
if PF_simplified == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')