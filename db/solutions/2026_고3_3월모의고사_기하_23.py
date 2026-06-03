import sympy as sp
from sympy import symbols, sqrt, solve, simplify

# 포물선 y^2 = 20x 위의 임의의 점 (x, y)는 초점까지의 거리 = 준선까지의 거리를 만족
x, y, p = symbols('x y p', real=True, positive=True)

# p = 5일 때 검증
p_val = 5

# 포물선 위의 점 예: y^2 = 20x에서 x = 5일 때
test_x = 5
test_y_sq = 20 * test_x  # y^2 = 100, y = ±10

# 초점 (5, 0)까지의 거리
focus_dist_sq = (test_x - p_val)**2 + test_y_sq  # (5-5)^2 + 100 = 100
focus_dist = sqrt(focus_dist_sq)  # sqrt(100) = 10

# 준선 x = -5까지의 거리
directrix_dist = test_x - (-p_val)  # 5 + 5 = 10

if simplify(focus_dist - directrix_dist) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')