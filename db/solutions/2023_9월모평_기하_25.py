from sympy import *

# Ellipse: x^2/9 + y^2/5 = 1, F=(2,0), F'=(-2,0)
a_val = 3
c_val = 2
F = Matrix([2, 0])
Fp = Matrix([-2, 0])
A = Matrix([2, 3])

# Verify given conditions
assert (A - F).norm() == 3, 'AF != 3'
assert (A - Fp).norm() == 5, 'AF\' != 5'

# Find P on segment AF' and on ellipse x^2/9 + y^2/5 = 1
x = symbols('x')
y_line = Rational(3,4)*(x+2)
ellipse_eq = x**2/9 + y_line**2/5 - 1
roots = solve(ellipse_eq, x)

P = None
for xr in roots:
    yr = y_line.subs(x, xr)
    pt = Matrix([xr, yr])
    # Check on segment: param t in [0,1] where A+t*(Fp-A)
    diff = pt - A
    ref = Fp - A
    t_val = diff[0] / ref[0]
    if 0 <= t_val <= 1:
        P = pt

assert P is not None, 'P not found on segment'

# Verify P is on ellipse
check = P[0]**2/9 + P[1]**2/5
assert simplify(check - 1) == 0, 'P not on ellipse'

# Compute perimeter
PF = (P - F).norm()
PFp = (P - Fp).norm()
FFp = (F - Fp).norm()
perimeter = simplify(PF + PFp + FFp)

if perimeter == 10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: perimeter={perimeter}')
