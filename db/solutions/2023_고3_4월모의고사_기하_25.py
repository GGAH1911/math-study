import sympy as sp
from sympy import sqrt, Rational

# 타원의 방정식 확인
x0, y0 = 4, 3
ellipse_check = x0**2 / 40 + y0**2 / 15
print(f'P on ellipse: {ellipse_check} == 1: {ellipse_check == 1}')

# 초점과 Q 확인
F_x = 5
Q_x = 40 / x0
OF = F_x
FQ = Q_x - F_x
print(f'OF = {OF}, FQ = {FQ}, OF == FQ: {OF == FQ}')

# 접선이 Q를 지나는지 확인
tangent_at_Q = (Q_x * x0) / 40 + (0 * y0) / 15
print(f'Tangent passes through Q: {tangent_at_Q} == 1: {tangent_at_Q == 1}')

# 삼각형 넓이
area = Rational(1, 2) * 10 * 3
print(f'Triangle area: {area}')

if area == 15 and ellipse_check == 1 and OF == FQ and tangent_at_Q == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')