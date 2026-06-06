import math
from sympy import *

# 원의 중심과 반지름
a, b = 1, sqrt(5)
r = b

# 조건 1: x축과의 접점
P = (a, 0)
print(f'P = {P}')

# 조건 2: y축과의 교점
Q = (0, b - sqrt(b**2 - a**2))
R = (0, b + sqrt(b**2 - a**2))
QR = simplify(sqrt((R[0]-Q[0])**2 + (R[1]-Q[1])**2))
print(f'QR = {QR}, 조건: QR=4, 만족: {QR == 4}')

# 조건 3: 점 P를 지나는 기울기 2 직선과 원의 교점
# 직선: y = 2(x - a)
# 원: (x-a)^2 + (y-b)^2 = b^2
x = symbols('x', real=True)
eq = (x - a)**2 + (2*(x - a) - b)**2 - b**2
sols = solve(eq, x)
print(f'직선과 원의 교점 x좌표: {sols}')

P_check = (float(sols[0]), 0)
S = (float(sols[1]), 2*(float(sols[1]) - a))
print(f'P = {P_check}, S = {S}')

# PS 거리
PS = sqrt((S[0] - P[0])**2 + (S[1] - P[1])**2)
PS_simplified = simplify(PS)
print(f'PS = {PS_simplified}, 조건: PS=4, 만족: {PS_simplified == 4}')

# 원점과 중심 사이의 거리
dist = sqrt(a**2 + b**2)
dist_simplified = simplify(dist)
print(f'원점과 중심 거리 = {dist_simplified}')

if dist_simplified == sqrt(6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')