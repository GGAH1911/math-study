from sympy import *
B = (0, 0); C = (4, 0)
cos_ABC = Rational(1, 8)
sin_ABC = sqrt(1 - cos_ABC**2)
A = (5*cos_ABC, 5*sin_ABC)
AC = sqrt((C[0]-A[0])**2 + (C[1]-A[1])**2)
print('AC =', AC)
D = ((4*A[0] + 5*C[0])/15, 4*A[1]/15)
O = (2, 6*sin_ABC/7)
R_sq = 4 + (6*sin_ABC/7)**2
t = symbols('t')
eq = (t*D[0]-2)**2 + (t*D[1]-O[1])**2 - R_sq
sols = solve(eq, t)
E = (3*D[0], 3*D[1])
EA = sqrt((E[0]-A[0])**2 + (E[1]-A[1])**2)
EC = sqrt((E[0]-C[0])**2 + (E[1]-C[1])**2)
ED = sqrt((E[0]-D[0])**2 + (E[1]-D[1])**2)
results = [AC == 6, EA == EC, ED == Rational(31,8)]
if all([bool(r) for r in results[:2]]) and not results[2]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')