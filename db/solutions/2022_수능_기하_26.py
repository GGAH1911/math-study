from sympy import *

c = 4*sqrt(3)
F = (c, S.Zero)
Fp = (-c, S.Zero)

y0 = Rational(3,2)*sqrt(3)
x0 = sqrt(64*(1 - y0**2/16))

A = (x0, y0)
B = (S.Zero, -3*y0)

# 1) A가 타원 위에 있는지 확인
assert simplify(x0**2/64 + y0**2/16 - 1) == 0, 'A not on ellipse'

# 2) 사각형 AFBF' 넓이 = 72 확인
x1,y1=A; x2,y2=F; x3,y3=B; x4,y4=Fp
area = Abs(x1*(y2-y4)+x2*(y3-y1)+x3*(y4-y2)+x4*(y1-y3))/2
assert simplify(area - 72) == 0, f'Area={area}'

# 3) 직선 AF: y0*x + (c-x0)*y - y0*c = 0
la, lb, lc_val = y0, c - x0, -y0*c
dist = Abs(la*B[0] + lb*B[1] + lc_val) / sqrt(la**2 + lb**2)
r = simplify(dist)

# 4) 직선 AF'까지 거리도 같은지 확인
lap, lbp, lcp = y0, -c - x0, y0*c
dist2 = Abs(lap*B[0] + lbp*B[1] + lcp) / sqrt(lap**2 + lbp**2)
r2 = simplify(dist2)
assert simplify(r - r2) == 0, 'distances not equal'

if simplify(r - 9) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: r={r}')
