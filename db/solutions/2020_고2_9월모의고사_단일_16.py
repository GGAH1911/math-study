from sympy import sqrt, symbols, solve

t = symbols('t', positive=True, real=True)
eq = t**2 - t - 12
sol_t = solve(eq, t)
t_val = [s for s in sol_t if s > 1][0]
d_val = t_val - 1

A = (0, 0)
B = (1, 0)
D = (float(d_val), 0)
E = (float(t_val)/2, float(t_val)*sqrt(3)/2)

DE_dist = sqrt((D[0] - E[0])**2 + (D[1] - E[1])**2)
if abs(DE_dist - sqrt(13)) < 1e-9:
    area = abs((B[0]*(D[1]-E[1]) + D[0]*(E[1]-B[1]) + E[0]*(B[1]-D[1]))/2)
    if abs(float(area) - float(2*sqrt(3))) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')