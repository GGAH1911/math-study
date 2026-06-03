from sympy import symbols, solve, simplify
a = 1
x = symbols('x')
quadratic = x**2 + a*x + a**2
line = -x
eq = quadratic - line
discriminant = eq.as_poly(x).discriminant()
roots = solve(eq, x)
if len(set(roots)) == 1 and discriminant == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')