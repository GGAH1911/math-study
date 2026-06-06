from sympy import *

CANDIDATE = 64

A = (6, 0)

cos_theta = Rational(5, 9)
sin_theta = sqrt(1 - cos_theta**2)
C = (6*cos_theta, 6*sin_theta)

AC_squared = (C[0] - A[0])**2 + (C[1] - A[1])**2
assert simplify(AC_squared - 32) == 0, "AC condition failed"

cos_theta_minus_phi = Rational(7, 9)
sin_theta_minus_phi = sqrt(1 - cos_theta_minus_phi**2)

cos_phi = cos_theta * cos_theta_minus_phi + sin_theta * sin_theta_minus_phi
sin_phi = sqrt(1 - cos_phi**2)
D = (6*cos_phi, 6*sin_phi)

CD_squared = (D[0] - C[0])**2 + (D[1] - C[1])**2
assert simplify(CD_squared - 16) == 0, "CD condition failed"

E_y = 6 * sin_phi
t_param = (E_y - 6*sin_theta) / (1 - cos_theta)
E = (C[0] + t_param*sin_theta, E_y)

CD = sqrt(CD_squared)
CE = sqrt((E[0] - C[0])**2 + (E[1] - C[1])**2)
ED = sqrt((D[0] - E[0])**2 + (D[1] - E[1])**2)

area_CED = abs((C[0]*(E[1] - D[1]) + E[0]*(D[1] - C[1]) + D[0]*(C[1] - E[1])) / 2)

R_circumcircle = (CD * CE * ED) / (4 * area_CED)
assert simplify(R_circumcircle**2 - 18) == 0, "Circumradius check failed"

AD_squared = (D[0] - A[0])**2 + (D[1] - A[1])**2

p = Rational(16, 3)
q = Rational(-4, 3)

expected_AD_squared = (p + q*sqrt(7))**2
assert simplify(expected_AD_squared - AD_squared) == 0, "AD form check failed"

result = 9 * abs(p * q)
assert result == CANDIDATE, f"Final answer {result} != CANDIDATE {CANDIDATE}"

print("VERIFY_PASS")