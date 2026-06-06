from sympy import symbols, solve, Eq
x, y = symbols('x y')
eq1 = Eq(2*x - y, 1)
eq2 = Eq(4*x**2 - x - y**2, 5)
sols = solve([eq1, eq2], [x, y])
alpha_beta_vals = [s[0]*s[1] for s in sols]
if 6 in alpha_beta_vals:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
