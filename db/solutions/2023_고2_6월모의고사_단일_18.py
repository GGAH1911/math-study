from sympy import *

t = Rational(2, 3)
k = 2**t  # 2^(2/3)

# 조건 확인
assert 1 < float(k) < 2, '범위 조건 실패'

# 각 점 좌표
Ax, Ay = Integer(-1), Integer(1)
Bx, By = Integer(1), Integer(1)
Cx, Cy = Integer(0), Integer(2)
Dx, Dy = t - 1, k
Ex, Ey = 1 - t, k
Fx, Fy = t, 2*k
Gx, Gy = -t, 2*k

# 원래 곡선에 각 점이 있는지 확인
assert simplify(2**(Dx+1) - Dy) == 0, 'D not on y=2^(x+1)'
assert simplify(2**(-Ex+1) - Ey) == 0, 'E not on y=2^(-x+1)'
assert simplify(2**(Fx+1) - Fy) == 0, 'F not on y=2^(x+1)'
assert simplify(2**(-Gx+1) - Gy) == 0, 'G not on y=2^(-x+1)'

# Shoelace 공식으로 넓이 계산
def shoelace(pts):
    n = len(pts)
    area = 0
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i+1)%n]
        area += x1*y2 - x2*y1
    return Abs(area)/2

area_ABED = shoelace([(Ax,Ay),(Bx,By),(Ex,Ey),(Dx,Dy)])
area_CFG  = shoelace([(Cx,Cy),(Fx,Fy),(Gx,Gy)])

diff = simplify(area_ABED - area_CFG)
if diff == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: diff={diff}')
