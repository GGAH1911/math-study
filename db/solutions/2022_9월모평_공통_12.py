import numpy as np
from sympy import *

R = 2*sqrt(7)
angle_A = pi/3
sin_BCD = 2*sqrt(7)/7

# BC 길이
BC = 2*R*sin(angle_A)

# 각 BDC (호 BC의 원주각)
angle_BDC = pi - angle_A

# cos(∠BCD)
cos_BCD = sqrt(1 - sin_BCD**2)

# 사인 법칙 비율
ratio = BC / sin(angle_BDC)

# BD
BD = ratio * sin_BCD
BD_val = simplify(BD)

# ∠DBC = π/3 - ∠BCD
# sin(∠DBC) = sin(π/3)cos(∠BCD) - cos(π/3)sin(∠BCD)
sin_DBC = sin(pi/3)*cos_BCD - cos(pi/3)*sin_BCD
sin_DBC_simplified = simplify(sin_DBC)

# CD
CD = ratio * sin_DBC_simplified
CD_val = simplify(CD)

# 답
answer = simplify(BD_val + CD_val)

if answer == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected 10, got {answer}')