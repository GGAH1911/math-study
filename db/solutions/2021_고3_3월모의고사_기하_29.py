from sympy import symbols, sqrt, Eq, solve, simplify
import numpy as np
from scipy.optimize import fsolve

# c값 선택 (예시: c=2)
c_val = 2.0

# 타원: x^2/9 + y^2/(9-c^2) = 1
# 쌍곡선: (x+1.5)^2/2.25 - y^2/(c^2+3c) = 1

def equations(vars):
    x, y = vars
    ellipse = x**2/9 + y**2/(9-c_val**2) - 1
    hyperbola = (x+1.5)**2/2.25 - y**2/(c_val**2 + 3*c_val) - 1
    return [ellipse, hyperbola]

# 제1사분면의 교점 찾기
P = fsolve(equations, [1.5, 2])
x_P, y_P = P

# 초점 정의
F1 = np.array([c_val, 0])
F2 = np.array([-c_val, 0])
F3 = np.array([-3-c_val, 0])
P_point = np.array([x_P, y_P])

# 거리 계산
PF1 = np.linalg.norm(P_point - F1)
PF2 = np.linalg.norm(P_point - F2)
PF3 = np.linalg.norm(P_point - F3)
F3F2 = np.linalg.norm(F3 - F2)

# 검증
ellipse_check = abs((PF1 + PF2) - 6) < 1e-6
hyperbola_check = abs((PF3 - PF1) - 3) < 1e-6
distance_check = abs(F3F2 - 3) < 1e-6
perimeter = PF3 + F3F2 + PF2
perimeter_check = abs(perimeter - 12) < 1e-6

if ellipse_check and hyperbola_check and distance_check and perimeter_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')