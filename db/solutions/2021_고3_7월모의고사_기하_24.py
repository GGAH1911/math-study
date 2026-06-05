from sympy import *
x, y = symbols('x y', real=True, positive=True)
a = 2/sqrt(3)
b = 1/sqrt(3)
# 원래 쌍곡선 조건 확인
cond1 = Eq(a**2 - b**2, 1)
# 접선 기울기 조건 확인 (dy/dx = x/y at P)
slope = a / b
cond2 = Eq(slope, 2)
# ab 값 확인
ab_val = a * b
if cond1 and cond2 and simplify(ab_val - Rational(2,3)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')