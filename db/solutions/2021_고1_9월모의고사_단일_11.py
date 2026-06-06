from sympy import symbols, Eq, solve
x, y = symbols('x y')
eq1 = Eq(4*x**2 - 4*x*y + y**2, 0)
eq2 = Eq(x + 2*y - 10, 0)
sols = solve([eq1, eq2], [x, y])
results = [a + b for a, b in sols]
if 6 in results:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')