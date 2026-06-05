import sympy as sp
from sympy import sqrt, symbols, solve

# 정의
x, y = symbols('x y', real=True)

# P의 좌표 검증
P_x = 4*sqrt(7)/7
P_y = 5*sqrt(21)/7

# 두 원의 조건 확인
dist_PF = sqrt((P_x - sqrt(7))**2 + P_y**2)
dist_PF_prime = sqrt((P_x + sqrt(7))**2 + P_y**2)

print('|PF| =', sp.simplify(dist_PF))
print('|PF\' =', sp.simplify(dist_PF_prime))
print('|FF\' =', 2*sqrt(7))

# Q의 좌표
Q_x = 104*sqrt(7)/91
Q_y = 39*sqrt(21)/91

# Q가 타원 위에 있는지 확인
ellipse_check = Q_x**2/16 + Q_y**2/9
print('Ellipse equation check:', sp.simplify(ellipse_check))

# Q가 직선 위에 있는지 확인 (F'을 지나고 FP에 수직)
line_check = Q_y - sqrt(3)*(Q_x + sqrt(7))/5
print('Line equation check:', sp.simplify(line_check))

# FQ의 길이
FQ_squared = (Q_x - sqrt(7))**2 + Q_y**2
FQ = sqrt(FQ_squared)
FQ_simplified = sp.simplify(FQ)
print('|FQ|² =', sp.simplify(FQ_squared))
print('|FQ| =', FQ_simplified)

if FQ_simplified == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')