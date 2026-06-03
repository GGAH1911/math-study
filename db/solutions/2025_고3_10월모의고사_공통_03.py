import sympy as sp
r_sq = sp.Rational(1, 2)
a1, a2, a3, a4, r = 8, 8*sp.sqrt(r_sq), 8*r_sq, 8*r_sq*sp.sqrt(r_sq), sp.sqrt(r_sq)
lhs = 8 * (8 * r_sq)
rhs = 2 * (8*sp.sqrt(r_sq)) * (8*r_sq*sp.sqrt(r_sq))
verify_eq = sp.simplify(lhs - rhs)
a5 = 8 * (r_sq)**2
print('VERIFY_PASS' if verify_eq == 0 and a5 == 2 else 'VERIFY_FAIL')