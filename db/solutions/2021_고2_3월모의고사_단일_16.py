from sympy import symbols, solve, simplify
k = -2
x, y = symbols('x y', real=True)
# 곡선 정의
curve = y - (k/(x-2) + 1)
# A: x축과의 교점 (y=0)
x_a = 2 - k
y_a = 0
result_a = curve.subs([(x, x_a), (y, y_a)])
# B: y축과의 교점 (x=0)
x_b = 0
y_b = 1 - k/2
result_b = curve.subs([(x, x_b), (y, y_b)])
# C: 점근선 교점
x_c, y_c = 2, 1
# 일직선 조건: 기울기가 같은지 확인
slope_ab = (y_b - y_a)/(x_b - x_a) if x_b != x_a else float('inf')
slope_ac = (y_c - y_a)/(x_c - x_a) if x_c != x_a else float('inf')
if slope_ab == slope_ac and result_a == 0 and result_b == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')