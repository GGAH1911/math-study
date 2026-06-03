from sympy import symbols, sqrt, Rational, solve, simplify
x, y = symbols('x y', real=True)
p = Rational(9, 10)
# Focus and directrix
F = (p, 0)
# A on parabola with AB = BF condition
a_sym = symbols('a', positive=True)
yA_sq = 4*p*a_sym
# AB = a + p, BF^2 = 4p^2 + 4pa
sol_a = solve((a_sym + p)**2 - (4*p**2 + 4*p*a_sym), a_sym)
A_x = [s for s in sol_a if s > 0][0]
A_y = sqrt(4*p*A_x)
A = (A_x, A_y)
B = (-p, A_y)
# Verify AB = BF
AB = sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)
BF = sqrt((B[0]-F[0])**2 + (B[1]-F[1])**2)
assert simplify(AB - BF) == 0
# Line BF intersect parabola y^2=4px
t = symbols('t', real=True)
# Parametrize from B to F
Lx = B[0] + t*(F[0]-B[0])
Ly = B[1] + t*(F[1]-B[1])
ts = solve(Ly**2 - 4*p*Lx, t)
# pick t in (0,1) for C on segment BF
C_t = [tv for tv in ts if 0 < tv < 1][0]
C = (B[0] + C_t*(F[0]-B[0]), B[1] + C_t*(F[1]-B[1]))
# Check on parabola
assert simplify(C[1]**2 - 4*p*C[0]) == 0
BC = sqrt((B[0]-C[0])**2 + (B[1]-C[1])**2)
CF = sqrt((C[0]-F[0])**2 + (C[1]-F[1])**2)
val = simplify(BC + 3*CF)
print('VERIFY_PASS' if val == 6 else 'VERIFY_FAIL')