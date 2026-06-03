from sympy import symbols, solve, simplify
r = symbols('r', positive=True, real=True)
eq = 3*r**4 + 2*r**2 - 1
r_sol = solve(eq, r)
a = 18
r_val = [x for x in r_sol if x > 0][0]
check_a3 = a * r_val**2
print('VERIFY_PASS' if abs(check_a3 - 6) < 1e-10 else 'VERIFY_FAIL')