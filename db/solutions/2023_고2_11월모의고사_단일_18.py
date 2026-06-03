import math
from sympy import symbols, cos, sin, sqrt, pi, simplify

# 주어진 값들
a = math.sqrt(15)
cos_theta = -1/4
sin_theta = math.sqrt(15)/4

# 검증 1: MN = AB 확인
AB = 2*a
M = (a, 0)
N = (3*a/2 * cos_theta, 3*a/2 * sin_theta)
MN = math.sqrt((N[0] - M[0])**2 + (N[1] - M[1])**2)
check1 = abs(MN - AB) < 1e-9

# 검증 2: 외접원 반지름 = 4
AM = a
AN = 3*a/2
K_AMN = 0.5 * a * (3*a/2) * sin_theta
R = (AM * AN * MN) / (4 * K_AMN)
check2 = abs(R - 4) < 1e-9

# 검증 3: 삼각형 ABC의 넓이
AC = 4*a
K_ABC = 0.5 * AB * AC * sin_theta
expected = 15 * math.sqrt(15)
check3 = abs(K_ABC - expected) < 1e-9

if check1 and check2 and check3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')