import sympy as sp

xP = sp.Rational(4, 1)
yP = sp.Rational(6, 1)
F = (sp.Rational(9, 4), sp.Integer(0))

# P가 포물선 y^2=9x 위에 있는지
assert yP**2 == 9*xP, 'P not on parabola'

# PF 확인
PF = sp.sqrt((xP - F[0])**2 + (yP - F[1])**2)
assert PF == sp.Rational(25, 4), f'PF={PF}'

# 포물선 접선 at P: yy1=(9/2)(x+x1) -> y=(3/4)x+3
# F'(-c,0)이 접선 위: 0=(3/4)(-c)+3 -> c=4
c = sp.Integer(4)
Fp = (-c, sp.Integer(0))
assert sp.Rational(3,4)*(-c) + 3 == 0, 'Tangent check failed'

# PF'
PFp = sp.sqrt((xP - Fp[0])**2 + (yP - Fp[1])**2)
assert PFp == 10, f'PFp={PFp}'

# 타원: 2a = PF + PF'
two_a = PF + PFp
a = two_a / 2  # 65/8

# 두 초점 간 거리 -> c_ellipse
dist_foci = sp.Abs(F[0] - Fp[0])
c_e = dist_foci / 2  # 25/8

# b^2 = a^2 - c_e^2
b_sq = a**2 - c_e**2  # 225/4
b = sp.sqrt(b_sq)      # 15/2
minor_axis = 2*b       # 15

if minor_axis == 15:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: minor_axis={minor_axis}')
