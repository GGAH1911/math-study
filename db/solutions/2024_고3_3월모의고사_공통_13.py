from sympy import *
a_sym = symbols('a', positive=True)
cos_B = Rational(-5, 8)
AB = a_sym; BC = 2*a_sym
AC_sq = AB**2 + BC**2 - 2*AB*BC*cos_B
AC = sqrt(AC_sq)
cos_half_B = sqrt((1 + cos_B) / 2)
QA_expr = simplify(AC / (2 * cos_half_B))
a_val = solve(QA_expr - 6*sqrt(10), a_sym)[0]
BC_val = 2 * a_val
angle_CDB = Rational(2, 3) * pi
R_CDB = simplify(BC_val / (2 * sin(angle_CDB)))
result = simplify(R_CDB - 4*sqrt(3))
print('VERIFY_PASS' if result == 0 else f'VERIFY_FAIL: got {R_CDB}')