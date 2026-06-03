import numpy as np
from sympy import *

x, y = symbols('x y', real=True)

# 타원 방정식: x^2/3 + (y-1)^2/4 = 1
# 초점 O(0,0), A(0,2), 2a=4

O = Matrix([0, 0])
A = Matrix([0, 2])

M_val = 3   # 최댓값
m_val = -1  # 최솟값

# M=3 검증: (0,3)이 타원 위에 있고 OQ+QA=4 만족?
Q_max = Matrix([0, M_val])
Q_min = Matrix([0, m_val])

def check_ellipse(Q):
    dist_O = sqrt((Q[0]-O[0])**2 + (Q[1]-O[1])**2)
    dist_A = sqrt((Q[0]-A[0])**2 + (Q[1]-A[1])**2)
    total = dist_O + dist_A
    return simplify(total - 4) == 0

def check_on_ellipse_eq(Q):
    return simplify(Q[0]**2/3 + (Q[1]-1)**2/4 - 1) == 0

# P0 검증
P0 = Matrix([Rational(-3,2), 0])
dist_OP0 = sqrt(P0[0]**2 + P0[1]**2)
dist_P0A = sqrt((P0[0]-A[0])**2 + (P0[1]-A[1])**2)
parabola_check = simplify((P0[1]-2)**2 - 8*(P0[0]+2)) == 0
sum_check = simplify(dist_OP0 + dist_P0A - 4) == 0

# 타원에서 y 최대/최소 확인
# y 최대: x=0, (y-1)^2/4=1 → y=3 or y=-1
# M=3 at (0,3), m=-1 at (0,-1)
check_M = check_ellipse(Q_max) and check_on_ellipse_eq(Q_max)
check_m = check_ellipse(Q_min) and check_on_ellipse_eq(Q_min)

# y가 타원에서 3보다 클 수 없음: (y-1)^2/4 <= 1 → -1<=y<=3
y_sym = symbols('y_sym', real=True)
y_range = solve((y_sym-1)**2/4 - 1, y_sym)  # boundary

result = M_val**2 + m_val**2  # = 10

if parabola_check and sum_check and check_M and check_m and result == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'parabola_check={parabola_check}, sum_check={sum_check}, check_M={check_M}, check_m={check_m}, result={result}')
