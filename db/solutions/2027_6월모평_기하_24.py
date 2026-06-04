from sympy import symbols, solve, simplify

# 포물선 y^2 = -12x
# 표준형 y^2 = 4ax 에서 4a = -12 => a = -3
# 초점 (a, 0) = (-3, 0) => p = -3

p = -3

# 검증: 포물선 y^2 = -12x 위의 점에서 초점까지의 거리 = 준선까지의 거리
# 초점 (p, 0) = (-3, 0), 준선 x = -p = 3
# 포물선 위의 임의의 점 (x0, y0): y0^2 = -12*x0
# 초점까지 거리: sqrt((x0 - p)^2 + y0^2)
# 준선까지 거리: |x0 + 3|

import sympy as sp

x0 = sp.Symbol('x0', real=True, negative=True)  # x0 < 0 for y^2 = -12x to have real y
y0_sq = -12 * x0  # y0^2

focus_x = p  # -3
directrix_x = -p  # 3

dist_focus_sq = (x0 - focus_x)**2 + y0_sq
dist_directrix = (x0 - directrix_x)**2  # (x0 - 3)^2, x0 < 0 so x0-3 < 0, |x0-3| = 3-x0

diff = sp.expand(dist_focus_sq - dist_directrix)
# Should be 0 for all x0
print('차이 (0이면 검증 통과):', sp.simplify(diff))

if sp.simplify(diff) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
