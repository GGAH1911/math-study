from sympy import *
theta = symbols('theta', positive=True)
# B=(0,0), C=(2,0), A=(cos θ, sin θ), AB=1, BC=2, angle CBA=θ
# D=(1,0): 중점연결정리 (M=AC중점, DM∥AB → D=BC중점)
# E: 각의이등분선정리 BE/EC = AB/AC = 1/sqrt(5-4cosθ)
AC_len = sqrt(5 - 4*cos(theta))
BE = Rational(2,1) / (1 + AC_len)
f_theta = Rational(1,2) * BE * sin(theta)  # 삼각형ABE 넓이
# t=(1-sqrt(5-4cosθ))/2 < 0, F=D+t*(cosθ,sinθ)
t_F = (1 - AC_len) / 2
g_theta = Rational(1,2) * 1 * (-t_F) * sin(theta)  # 삼각형DFC 넓이
# 극한 계산
ratio = g_theta / (theta**2 * f_theta)
ratio_simplified = simplify(ratio)
L = limit(ratio_simplified, theta, 0, '+')
if L == Rational(1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', 'got', L)