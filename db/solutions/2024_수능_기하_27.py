from sympy import *
t_val = 2*sqrt(2)
A = (2*t_val**2, 4*t_val)
B = Rational(-2, 1), 4*t_val
F = (Rational(2,1), Rational(0,1))
x = symbols('x')
quad = t_val**2 * x**2 - 4*(t_val**2 + 2)*x + 4*t_val**2
sols = sorted(solve(quad, x))
x_C, x_D = sols[0], sols[1]
y_C = -t_val*(x_C - 2)
y_D = -t_val*(x_D - 2)
C = (x_C, y_C); D = (x_D, y_D)
assert simplify(y_C**2 - 8*x_C) == 0, 'C not on parabola'
assert simplify(y_D**2 - 8*x_D) == 0, 'D not on parabola'
BC = sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2)
CD = sqrt((D[0]-C[0])**2 + (D[1]-C[1])**2)
assert simplify(BC - CD) == 0, 'BC != CD'
CF = sqrt((C[0]-F[0])**2 + (C[1]-F[1])**2)
DF = sqrt((D[0]-F[0])**2 + (D[1]-F[1])**2)
assert simplify(CF - DF) < 0, 'CF not < DF'
ax,ay = A; bx,by = B; dx,dy = D
area = Rational(1,2)*Abs(ax*(by-dy)+bx*(dy-ay)+dx*(ay-by))
if simplify(area - 108*sqrt(2)) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {simplify(area)}')