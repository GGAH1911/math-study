from sympy import *
sqrt3 = sqrt(3)
A = Matrix([6, 6*sqrt3])
B = Matrix([0, 0])
C = Matrix([12, 0])
D = Matrix([8, 0])
# Verify DC=4
assert (C-D).norm() == 4, 'DC check fail'
# Build equilateral triangle ADE: rotate D around A by +60 deg
theta = pi/3
DA = D - A
Ex = cos(theta)*DA[0] - sin(theta)*DA[1] + A[0]
Ey = sin(theta)*DA[0] + cos(theta)*DA[1] + A[1]
E = simplify(Matrix([Ex, Ey]))
assert simplify((E-A).norm() - (D-A).norm()) == 0, 'ADE not equilateral'
assert simplify((D-E).norm() - (D-A).norm()) == 0, 'ADE not equilateral DE'
# Find F = intersection of AC and DE
t, s = symbols('t s')
F_expr = A + t*(C-A)
DE_expr = D + s*(E-D)
sol = solve([F_expr[0]-DE_expr[0], F_expr[1]-DE_expr[1]], [t,s])
t_val = sol[t]
F = simplify(A + t_val*(C-A))
# CE, CF
CE_val = simplify((E-C).norm())
CF_val = simplify((F-C).norm())
p_val = CE_val
q_val = Rational(3)
r_val = CF_val
total = simplify(p_val + q_val + r_val)
# Check similarity ratio AC:EC = 3:2
ratio = simplify(Rational(12,1)/CE_val)
if (simplify(p_val - 8) == 0 and
    simplify(r_val - Rational(8,3)) == 0 and
    simplify(ratio - Rational(3,2)) == 0 and
    simplify(total - Rational(41,3)) == 0):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('CE=', CE_val, 'CF=', CF_val, 'total=', total)
