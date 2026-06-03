import sympy as sp

# 포물선: y^2 = 8x
# 표준형: y^2 = 4px, 초점 (p, 0)
# 8 = 4p 이므로 p = 2

p = 2

# 초점: (p, 0) = (2, 0)
focus_x = p

# 검증: 포물선 방정식 y^2 = 8x에서
# 임의의 점 (x, y)에서 초점까지 거리 = x + p (준선까지 거리)
# 초점 (p, 0)까지 거리 = sqrt((x-p)^2 + y^2)
# 준선 x = -p까지 거리 = x + p

x, y = sp.symbols('x y', real=True)

# 포물선 위의 점에서 초점까지 거리
focus_distance = sp.sqrt((x - p)**2 + y**2)

# 준선까지 거리
directrix_distance = x + p

# y^2 = 8x를 대입하면
y_sq = 8*x

# 초점까지 거리^2 = (x - p)^2 + y^2 = (x - p)^2 + 8x
dist_sq = (x - p)**2 + 8*x
dist_sq_expanded = sp.expand(dist_sq)

# 정리하면: (x - 2)^2 + 8x = x^2 - 4x + 4 + 8x = x^2 + 4x + 4 = (x + 2)^2
dist_sq_factored = sp.factor(dist_sq_expanded)

# 따라서 초점까지 거리 = x + 2 = 준선까지 거리
# 이는 포물선의 정의를 만족

if dist_sq_factored == (x + 2)**2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')