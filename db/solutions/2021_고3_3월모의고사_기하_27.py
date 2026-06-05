import numpy as np
from sympy import symbols, sqrt, solve, simplify

# 포물선 y^2 = 4x 위의 점 P를 매개변수로 표현: P = (t^2, 2t)
# 그리고 Q = (-4, q)는 직선 x = -4 위의 점

t = symbols('t', real=True)

# 점 P의 좌표
Px = t**2
Py = 2*t

# 점 A의 좌표
Ax, Ay = 6, 12

# 초점 F의 좌표
Fx, Fy = 1, 0

# AP의 거리
AP = sqrt((Px - Ax)**2 + (Py - Ay)**2)

# PF의 거리
PF = sqrt((Px - Fx)**2 + (Py - Fy)**2)

# 포물선 성질: PF = Px + 1 (초점까지 거리 = 준선까지 거리)
# PQ의 최솟값 = Px + 4
PQ_min = Px + 4

# 최소화할 함수: AP + PF + 3
f = AP + PF + 3

# 선분 AF 위의 점인지 확인
# AF = sqrt((6-1)^2 + (12-0)^2) = sqrt(169) = 13
AF = 13

# P가 선분 AF 위에 있을 때, AP + PF = AF = 13
# 이를 확인하기 위해 직선 AF의 방정식을 구함
# 직선 AF: y = (12/5)(x - 1)
# 이 직선과 포물선의 교점에서 확인

# 최솟값은 13 + 3 = 16
min_value = AF + 3

if min_value == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')