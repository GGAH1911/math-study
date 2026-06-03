from sympy import *
a = symbols('a', positive=True)
# 원래 함수 정의
# A: y=a/x 와 y=6 교점
xA = a / 6
yA = 6
# B: y=-2a/x 와 y=6 교점
xB = -a / 3
yB = 6
# C: 직선 OA (y = 36/a * x) 와 y=3 교점
xC = a / 12
yC = 3
# D: 직선 OB (y = -18/a * x) 와 y=3 교점
xD = -a / 6
yD = 3
# 사다리꼴 넓이 (사각형 ABDC, 쇼레이스 공식)
area_expr = Rational(1,2)*Abs(
    xA*(yB - yC) + xB*(yD - yA) + xD*(yC - yB) + xC*(yA - yD)
)
area_simplified = simplify(area_expr.subs(a, Symbol('a', positive=True)))
# a=24 대입
a_val = 24
area_val = area_expr.subs(a, a_val)
if area_val == 27:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area={area_val}')
