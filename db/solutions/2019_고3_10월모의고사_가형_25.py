import numpy as np
from sympy import *

CANDIDATE = 18

# 타원 정의
x, y = symbols('x y', real=True)
ellipse_eq = x**2/12 + y**2/16 - 1

# 접점 B(0, 4)
B = (0, 4)
verify_B_ellipse = ellipse_eq.subs([(x, B[0]), (y, B[1])])
tangent_B = x*B[0]/12 + y*B[1]/16 - 1
verify_B_tangent = tangent_B.subs([(x, 6), (y, 4)])

# 접점 C(3, -2)
C = (3, -2)
verify_C_ellipse = ellipse_eq.subs([(x, C[0]), (y, C[1])])
tangent_C = x*C[0]/12 + y*C[1]/16 - 1
verify_C_tangent = tangent_C.subs([(x, 6), (y, 4)])

# 넓이 계산 (좌표 공식)
A = (6, 4)
area = abs((A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1]))/2)

if area == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')