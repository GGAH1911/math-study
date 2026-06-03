import math
from sympy import symbols, sqrt, simplify, Rational

a = Rational(9, 2)

# 좌표 설정
A = (0, a)
P = (a, 0)
Q = (8, 8 - a)
D = (8, a)

# 신발끈 공식으로 사각형 APQD의 넓이 계산
area_2x = abs((A[0]*P[1] - P[0]*A[1]) + (P[0]*Q[1] - Q[0]*P[1]) + (Q[0]*D[1] - D[0]*Q[1]) + (D[0]*A[1] - A[0]*D[1]))
area = area_2x / 2

target_area = Rational(79, 4)

if area == target_area:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')