from sympy import *

a_val = Rational(9, 8)
c_val = Rational(15, 8)
b_sq = c_val**2 - a_val**2
b_val = sqrt(b_sq)

A_pt = Matrix([0, b_val * c_val / a_val])
F_pt = Matrix([c_val, 0])

t_P = (a_val**2 + c_val**2) / (2 * a_val * c_val)
P_pt = Matrix([t_P * a_val, b_val * c_val / a_val - t_P * b_val])

t_Pp = (a_val**2 + c_val**2) / (2 * c_val**2)
P_prime_pt = Matrix([-c_val * t_Pp, b_val * c_val / a_val * (1 - t_Pp)])

hyp_P = simplify(P_pt[0]**2 / a_val**2 - P_pt[1]**2 / b_sq - 1)
hyp_Pp = simplify(P_prime_pt[0]**2 / a_val**2 - P_prime_pt[1]**2 / b_sq - 1)

AP = simplify((P_pt - A_pt).norm())
PF = simplify((F_pt - P_pt).norm())
PP_prime = simplify((P_prime_pt - P_pt).norm())

ok = (
    hyp_P == 0 and
    hyp_Pp == 0 and
    simplify(PF - 1) == 0 and
    simplify(AP / PP_prime - Rational(5, 6)) == 0
)
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
