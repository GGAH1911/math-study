from sympy import *
import math

# 원래 문제의 타원 방정식
x, y, a = symbols('x y a', real=True, positive=True)

# 점 (√3, -2)가 타원 위에 있다는 조건
point_x = sqrt(3)
point_y = -2

# a 구하기
eq = point_x**2 / a**2 + point_y**2 / 6 - 1
a_val = solve(eq, a)[0]  # a = 3

# 접선 공식으로 기울기 구하기
# 타원 x²/9 + y²/6 = 1의 점 (√3, -2)에서의 접선
# (√3·x)/9 + (-2·y)/6 = 1
# (√3·x)/9 - y/3 = 1
# -y/3 = 1 - (√3·x)/9
# y = -3 + (√3/3)·x

slope = sqrt(3)/3

# 검증: 점 (√3, -2)를 직선에 대입
y_on_tangent = -3 + slope * sqrt(3)

verify_result = simplify(y_on_tangent - point_y)

if verify_result == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')