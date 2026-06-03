from sympy import symbols, solve, Eq
x, y = symbols('x y')
eq1 = Eq(x - y, 2)
eq2 = Eq(x**2 + 8*x + y**2, 2)
sols = solve([eq1, eq2], [x, y])
alpha_plus_beta = [s[0] + s[1] for s in sols]
if all(v == -4 for v in alpha_plus_beta):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', alpha_plus_beta)
