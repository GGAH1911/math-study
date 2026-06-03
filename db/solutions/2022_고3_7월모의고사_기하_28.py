from sympy import *
a_val = 4*sqrt(3); b_val = 2*sqrt(3)
A = Matrix([Rational(3,2), 0]); F = Matrix([6, 0]); Fp = Matrix([-6, 0]); P = Matrix([2, sqrt(11)])
assert simplify(P[0]**2/a_val**2 + P[1]**2/b_val**2 - 1) == 0, 'VERIFY_FAIL: not on ellipse'
PA = A - P; PF_v = F - P; PFp_v = Fp - P
cos1 = simplify(PA.dot(PF_v)/(PA.norm()*PF_v.norm()))
cos2 = simplify(PA.dot(PFp_v)/(PA.norm()*PFp_v.norm()))
assert simplify(cos1 - cos2) == 0, 'VERIFY_FAIL: angle bisector'
t = symbols('t'); Bpt = A + t*(P - A)
t_sol = solve((Bpt - F).dot(P - A), t)[0]
B = A + t_sol*(P - A)
assert simplify(B.norm()**2 - 3) == 0, 'VERIFY_FAIL: OB!=sqrt(3)'
assert simplify(a_val*b_val - 24) == 0, 'VERIFY_FAIL: a*b!=24'
print('VERIFY_PASS')