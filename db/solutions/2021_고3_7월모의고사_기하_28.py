from sympy import *
m_val = sqrt(5)/2
m2 = Rational(5,4)
# F, A, B
F = (1, 0); A = (1, 2); B = (1, -2)
# x_C, x_D from quadratic m^2*x^2 - (2m^2+4)x + m^2 = 0
a_c = m2
b_c = -(2*m2 + 4)
c_c = m2
disc = sqrt(b_c**2 - 4*a_c*c_c)
x_C = (-b_c + disc)/(2*a_c)
x_D = (-b_c - disc)/(2*a_c)
y_C = m_val*(x_C - 1)
y_D = m_val*(x_D - 1)
# verify on parabola
assert simplify(y_C**2 - 4*x_C) == 0
assert simplify(y_D**2 - 4*x_D) == 0
# areas
S_FCA = Rational(1,2)*2*abs(x_C - 1)
S_FDB = Rational(1,2)*2*abs(x_D - 1)
ratio = simplify(S_FCA / S_FDB)
if ratio == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', ratio)
