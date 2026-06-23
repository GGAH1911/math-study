from sympy import *
t = symbols('t', real=True)

# r_triangle(t)^2 = 12/cos^2(t - pi/6)
r_tri_sq = 12 / cos(t - pi/6)**2

# Area alpha: sector slice [0, pi/3] minus triangle slice [0, pi/3]
sector_1 = Rational(1,2) * 16 * pi / 3  # = 8pi/3
tri_1 = Rational(1,2) * integrate(r_tri_sq, (t, 0, pi/3))  # = 4sqrt(3)
alpha = simplify(sector_1 - tri_1)

# Area beta: triangle slice [pi/3, pi/2] minus sector slice [pi/3, pi/2]
tri_2 = Rational(1,2) * integrate(r_tri_sq, (t, pi/3, pi/2))  # = 4sqrt(3)
sector_2 = Rational(1,2) * 16 * (pi/2 - pi/3)  # = 4pi/3
beta = simplify(tri_2 - sector_2)

# S1
S1 = simplify(alpha + beta)  # should be 4pi/3

# Scale factor: B2=(0,4), A2=(4/sqrt(3),0)
# k = (4/sqrt(3))/4 = 1/sqrt(3), area_ratio = 1/3
area_ratio = Rational(1, 3)

# Limit
lim_Sn = simplify(S1 / (1 - area_ratio))

if simplify(lim_Sn - 2*pi) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: S1={S1}, lim_Sn={lim_Sn}')
