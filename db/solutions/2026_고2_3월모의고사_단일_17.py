import sympy as sp
import numpy as np

m = 2 - sp.sqrt(3)

# H 점
H_x = 3 * (1 + m) / (m**2 + 1)
H_y = 3 * m * (1 + m) / (m**2 + 1)
OH = sp.sqrt(H_x**2 + H_y**2)
OH = sp.simplify(OH)

# 교점 B
a = 1 + m**2
b = -6 * (1 + m)
c = 9
delt = b**2 - 4*a*c
x_B = (-b - sp.sqrt(delt)) / (2*a)
y_B = m * x_B
OB = sp.sqrt(x_B**2 + y_B**2)
OB = sp.simplify(OB)

# B가 원 위에 있는지 확인
dist_sq = (x_B - 3)**2 + (y_B - 3)**2
dist_sq = sp.simplify(dist_sq)

# BH와 비율
BH = OH - OB
BH = sp.simplify(BH)
ratio = sp.simplify(OH / BH)

# 수치 검증
m_num = float((2 - np.sqrt(3)))
OH_num = float(OH.evalf())
BH_num = float(BH.evalf())
ratio_num = OH_num / BH_num

# B가 원 위에 있는가
x_B_num = float(x_B.evalf())
y_B_num = float(y_B.evalf())
radius_check = float(np.sqrt((x_B_num - 3)**2 + (y_B_num - 3)**2))

if np.isclose(ratio_num, np.sqrt(3), rtol=1e-9) and np.isclose(radius_check, 3.0, rtol=1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')