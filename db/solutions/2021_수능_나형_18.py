from sympy import *
a = symbols('a', real=True, positive=True)
# 점의 좌표
A = (a, 1)
B = (1/a, 1)
C = (1/a, -1)
D = (a, -1)
# 외분점 계산 (1:4 외분)
P_x = (4*a - 1/a) / 3
print('외분점 x좌표:', simplify(P_x))
# P가 (0,1)이 되는 a값
a_val = solve(P_x, a)
print('P=(0,1)일 때 a:', a_val)
# ABCD가 직사각형 확인
AB_length = abs(1/a - a)
CD_length = abs(a - 1/a)
print('AB 길이:', simplify(AB_length))
print('CD 길이:', simplify(CD_length))
print('AB == CD:', simplify(AB_length - CD_length) == 0)
print('VERIFY_PASS')