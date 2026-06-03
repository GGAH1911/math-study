from sympy import symbols, solve, Eq
x, y = symbols('x y')
eq1 = Eq(x - y + 1, 0)
eq2 = Eq(x**2 - 2*y**2 - 2, 0)
sols = solve([eq1, eq2], [x, y])
alpha_beta_values = [s[0] + s[1] for s in sols]
expected = -3
if all(v == expected for v in alpha_beta_values) and len(alpha_beta_values) > 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', alpha_beta_values)