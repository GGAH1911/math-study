from sympy import symbols, solve, Eq
x, y = symbols('x y', real=True)
eq1 = Eq(2*x - y, 1)
eq2 = Eq(5*x**2 - y**2, -5)
sols = solve([eq1, eq2], [x, y])
alpha, beta = sols[0]
result = alpha - beta
if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')