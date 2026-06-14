import sympy as sp
from sympy import symbols, diff

CANDIDATE = 7

x = symbols('x')
y = 4*x**3 - 5*x + 9
y_prime = diff(y, x)

# 점 (1, 8)이 곡선 위의 점 확인
point_on_curve = y.subs(x, 1) == 8

# x=1에서의 도함수값(접선의 기울기)
slope_at_1 = y_prime.subs(x, 1)

if slope_at_1 == CANDIDATE and point_on_curve:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')