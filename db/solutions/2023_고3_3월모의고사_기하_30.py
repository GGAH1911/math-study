import numpy as np
from scipy.optimize import fsolve

# c 값으로부터 타원·쌍곡선 구성
c = 5*np.sqrt(3)/6
a = np.sqrt(3)*c
b = np.sqrt(2)*c

# 타원: x^2/a^2 + y^2/b^2 = 1
A = np.array([c, b**2/a])
B = np.array([-c, b**2/a])
F = np.array([c, 0])
P = np.array([c, 2*b**2/a])

# 검증 1: A, B가 타원 위에 있는가?
verify1 = (A[0]**2/a**2 + A[1]**2/b**2 - 1) < 1e-10
verify2 = (B[0]**2/a**2 + B[1]**2/b**2 - 1) < 1e-10

# 검증 2: 삼각형 BFP가 정삼각형인가?
BF = np.linalg.norm(F - B)
FP = np.linalg.norm(P - F)
BP = np.linalg.norm(P - B)
verify3 = (abs(BF - FP) < 1e-10 and abs(FP - BP) < 1e-10)

# 검증 4: AF 계산
AF = np.linalg.norm(F - A)
result = 60 * AF

# 조건 (나) 검증: 장축 길이 - 삼각형 BQR 둘레 = 3
Q = np.array([-3*c/5, 8*np.sqrt(3)*c/15])
R = np.array([-3*c/5, 4*np.sqrt(3)*c/5])
BQ = np.linalg.norm(Q - B)
QR = np.linalg.norm(R - Q)
RB = np.linalg.norm(B - R)
perimeter_BQR = BQ + QR + RB
major_axis = 2*a
verify4 = abs(major_axis - perimeter_BQR - 3) < 1e-10

if verify1 and verify2 and verify3 and verify4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')