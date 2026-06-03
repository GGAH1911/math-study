from sympy import symbols, sqrt, Eq, simplify

# 원래 조건: 점 (a, 2)에서 초점 F(1/3, 0)까지 거리 = 준선 x=-1/3까지 거리
a = 3
focus_dist = sqrt((a - 1/3)**2 + (2 - 0)**2)
directrix_dist = abs(a - (-1/3))

if abs(focus_dist - directrix_dist) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
