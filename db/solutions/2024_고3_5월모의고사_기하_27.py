from sympy import *
x, y = symbols('x y', real=True)
# 포물선 y^2=4x, 초점 F=(1,0)
# 직선 x-y-2=0으로부터 거리가 k인 평행선 두 개
# 총 교점 수 3: c2=-1 조건 => k=3/sqrt(2)
k_val = Rational(3,1)/sqrt(2)
c2 = 2 - k_val*sqrt(2)  # -1
c1 = 2 + k_val*sqrt(2)  # 5
assert simplify(c2 + 1) == 0, 'c2 check fail'
assert simplify(c1 - 5) == 0, 'c1 check fail'
# L2 접점
y2 = solve(y**2 - 4*y - 4*c2, y)
assert len(y2)==1 and simplify(y2[0]-2)==0, 'L2 접점 check fail'
x2 = y2[0] + c2
assert simplify(y2[0]**2 - 4*x2)==0, 'L2 접점 포물선 위 check fail'
# L1 두 교점
y1s = solve(y**2 - 4*y - 4*c1, y)
assert len(y1s)==2, 'L1 교점 수 check fail'
pts = [(yv + c1, yv) for yv in y1s]
for px, py in pts:
    assert simplify(py**2 - 4*px)==0, 'L1 교점 포물선 위 check fail'
# 초점거리 합
all_pts = [(x2, y2[0])] + pts
total = sum(pt[0]+1 for pt in all_pts)
result = simplify(total)
if result == 18:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {result}')