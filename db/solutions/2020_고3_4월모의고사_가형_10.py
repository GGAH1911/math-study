import sympy as sp
from sympy import sqrt, pi, cos, sin

# r = 8로 설정
r = 8

# 좌표 설정
O = (0, 0)
A = (r, 0)
B = (r * cos(pi/3), r * sin(pi/3))
B_simplified = (r/2, r*sqrt(3)/2)

# P: OA를 3:1로 내분
P = (3*r/4, 0)

# Q: OB를 1:2로 내분
Q = (r/6, r*sqrt(3)/6)

# 삼각형 OPQ 넓이 계산
area_formula = sp.Rational(1,2) * abs(P[0] * Q[1] - Q[0] * P[1])
area_OPQ = area_formula.subs([(P[0], 3*r/4), (P[1], 0), (Q[0], r/6), (Q[1], r*sqrt(3)/6)])
area_OPQ = sp.Rational(1,2) * (3*r/4) * (r*sqrt(3)/6)
area_OPQ_simplified = area_OPQ.simplify()

# r=8 대입
area_value = area_OPQ_simplified.subs(r, 8)
area_value = area_value.simplify()

# 예상값: 4√3
expected_area = 4 * sqrt(3)

# 검증
if (area_value - expected_area).simplify() == 0:
    arc_length = r * pi / 3
    arc_length_value = arc_length.subs(r, 8)
    if arc_length_value == 8*pi/3:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')