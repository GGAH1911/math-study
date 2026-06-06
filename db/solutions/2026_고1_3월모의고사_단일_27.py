import numpy as np
from scipy.optimize import fsolve

# 정육각형 꼭짓점
A = np.array([np.sqrt(3)/2, 0.5])
F = np.array([np.sqrt(3)/2, -0.5])
E = np.array([0, -1])

# 정사각형에서 G
G = np.array([(np.sqrt(3)+1)/2, (1+np.sqrt(3))/2])

# 정오각형에서 H (FE를 108도 회전)
FE = E - F
angle = np.radians(108)
cos_a, sin_a = np.cos(angle), np.sin(angle)
FH = np.array([FE[0]*cos_a - FE[1]*sin_a, FE[0]*sin_a + FE[1]*cos_a])
H = F + FH

# 선분 AH: P = A + t(H-A), 선분 FG: Q = F + s(G-F)
def equations(vars):
    t, s = vars
    P = A + t*(H - A)
    Q = F + s*(G - F)
    return [P[0] - Q[0], P[1] - Q[1]]

from scipy.optimize import fsolve
t, s = fsolve(equations, [0.2, 0.3])
I = A + t*(H - A)

# 각도 계산
IA = A - I
IF = F - I
cos_angle = np.dot(IA, IF) / (np.linalg.norm(IA) * np.linalg.norm(IF))
angle_rad = np.arccos(cos_angle)
angle_deg = np.degrees(angle_rad)

if abs(angle_deg - 141) < 1:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {angle_deg:.1f}°')