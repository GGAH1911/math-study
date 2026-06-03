from sympy import *

h = symbols('h', positive=True)

# Coordinates
A_p = Matrix([-3, 0, 0])
B_p = Matrix([3, 0, 0])
P = Matrix([0, 6, 0])
A = Matrix([-3, 0, h])
B = Matrix([3, 0, h])
M = Matrix([0, 0, h])
M_p = Matrix([0, 0, 0])

# Verify given conditions
cond1 = simplify((B-A).norm() - 6) == 0  # AB = 6
cond2 = simplify((B_p-A_p).norm() - 6) == 0  # A'B' = 6
cond3 = (M_p-P).dot(B_p-A_p) == 0  # PM' perp A'B'
cond4 = simplify((M_p-P).norm() - 6) == 0  # PM' = 6

# Normal to alpha (A'B'P plane)
n1 = Matrix([0, 0, 1])

# Normal to plane ABP
n2 = (B-A).cross(P-A)

# cos theta between planes
cos_theta = simplify(Abs(n1.dot(n2)) / (n1.norm() * n2.norm()))

# Area of A'B'P
area_orig = Rational(1,2) * 6 * 6  # = 18

# Solve: area_orig * cos_theta = 9/2
sol_h = solve(Eq(area_orig * cos_theta, Rational(9,2)), h)

if not sol_h:
    print('VERIFY_FAIL: no solution for h')
else:
    h_val = sol_h[0]
    # Compute PM
    PM_val = simplify((M.subs(h, h_val) - P).norm())
    if PM_val == 24 and all([cond1, cond2, cond3, cond4]):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL:', PM_val)
