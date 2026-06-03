from sympy import symbols, Eq, solve, Rational, sqrt, Abs
x, y, X, Y = symbols('x y X Y', real=True)
# 원래 식: y^2 = 12(x-2)
# 정의: 초점 F=(a,b), 준선 l: x=c 라고 가정하고, 포물선 정의로부터 결정
# 포물선 위 임의의 점 (x,y)에서 초점까지의 거리 = 준선까지의 거리
# 식: sqrt((x-a)^2 + (y-b)^2) = |x - c|
# 제곱: (x-a)^2 + (y-b)^2 = (x-c)^2
# 전개: x^2 -2ax + a^2 + y^2 - 2by + b^2 = x^2 - 2cx + c^2
# => y^2 - 2by + b^2 + a^2 - 2ax + 2cx - c^2 = 0
# => y^2 = 2by - b^2 - a^2 + 2(a-c)x + c^2
# 원래식 y^2 = 12x - 24 와 항별 비교
# 계수: y^1: -2b = 0 => b=0
# 상수항(x=0): -b^2 - a^2 + c^2 = -24 => c^2 - a^2 = -24
# x계수: 2(a-c) = 12 => a - c = 6
# => (a-c)(a+c) = a^2 - c^2 = 24 => a+c = 4
# => a = 5, c = -1
a_sol, c_sol = 5, -1
# 초점: (5,0), 준선: x=-1
focus = (a_sol, 0)
directrix_x = c_sol
dist = abs(focus[0] - directrix_x)
# 검증: 포물선 위의 점에서 초점거리 == 준선거리 확인
import sympy as sp
x0 = sp.Rational(5,1)  # y^2 = 12*3 = 36, y=6
y0 = sp.sqrt(12*(x0-2))
d_focus = sp.sqrt((x0-focus[0])**2 + (y0-focus[1])**2)
d_dir = abs(x0 - directrix_x)
ans_candidate = 6
if sp.simplify(d_focus - d_dir) == 0 and dist == ans_candidate:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')