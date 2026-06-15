from sympy import symbols, solve, expand

a = 4
x = symbols('x')
eq = 2*x**2 - 6*x + (a - 12)
roots = solve(eq, x)
product = roots[0] * roots[1]
if abs(product - (-4)) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')