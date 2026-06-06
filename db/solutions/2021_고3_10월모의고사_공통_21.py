import math
from sympy import symbols, cos, sin, sqrt, simplify, atan2, pi

# θ를 매개변수로 하여 일반적으로 검증
theta = symbols('theta', real=True, positive=True)

# 삼각형 좌표
A = (0, 0)
B = (6, 0)
C = (8*cos(theta), 8*sin(theta))

# 외접원 중심
O_x = 3
O_y = (4 - 3*cos(theta)) / sin(theta)

# 각의 이등분선 위의 점
t = (6 + 8) / (2*cos(theta/2))
D_x = t * cos(theta/2)
D_y = t * sin(theta/2)

# AC 방향 단위벡터로 정사영
k = D_x * cos(theta) + D_y * sin(theta)
k_simplified = simplify(k)

# k = 7 확인
if simplify(k_simplified - 7) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')