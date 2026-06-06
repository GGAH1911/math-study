from sympy import symbols, solve, simplify
x, y = symbols('x y')
eq1 = 2*x - y - 1
eq2 = 4*x**2 - 6*y + 3
solutions = solve([eq1, eq2], [x, y])
alpha, beta = solutions[0][0], solutions[0][1]
product = alpha * beta
result = simplify(product)
if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')