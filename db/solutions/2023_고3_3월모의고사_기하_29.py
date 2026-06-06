import sympy as sp
from sympy import sqrt, solve, symbols

p_val = sp.Rational(96, 25)

# 점 P
P_x = p_val / 4
P_y = p_val

# 원의 중심
a = 3 - p_val
b = -4 + 8*p_val/3

# 검증 1: 중심이 직선 FP 위
y_on_line = -sp.Rational(4,3) * (a - p_val)
check1 = (b - y_on_line == 0)

# 검증 2: 원이 점 P를 지남 (반지름 = 3)
dist_P = sqrt((a - P_x)**2 + (b - P_y)**2)
check2 = (dist_P - 3 == 0)

# 검증 3: 준선 x = -p에 접함 (거리 = 3)
dist_directrix = a - (-p_val)
check3 = (dist_directrix - 3 == 0)

# 검증 4: 중심의 x좌표 < P의 x좌표
check4 = (a < P_x)

if check1 and check2 and check3 and check4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')