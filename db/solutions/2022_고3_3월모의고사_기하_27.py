from sympy import *
import math

p = sqrt(2)
y_P = 2*sqrt(3)*p

# 점들의 좌표
P = (3*p, y_P)
Q = (p/3, y_P/3)
F = (p, 0)

# Q가 포물선 y^2 = 4px 위에 있는지 확인
y_Q = Q[1]
x_Q = Q[0]
parabola_check = (y_Q**2 - 4*p*x_Q).simplify()

# Q가 선분 FH를 1:2로 내분하는지 확인
H = (-p, y_P)
Q_internal = ((2*F[0] + H[0])/3, (2*F[1] + H[1])/3)
internal_check = (Q[0] - Q_internal[0])**2 + (Q[1] - Q_internal[1])**2

# 삼각형 PQF의 넓이
area = abs((P[0]*(Q[1]-F[1]) + Q[0]*(F[1]-P[1]) + F[0]*(P[1]-Q[1]))/2)
area_simplified = area.simplify()
expected_area = 8*sqrt(3)/3
area_check = (area_simplified - expected_area).simplify()

if parabola_check == 0 and internal_check == 0 and area_check == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'parabola_check: {parabola_check}')
    print(f'internal_check: {internal_check}')
    print(f'area_check: {area_check}')