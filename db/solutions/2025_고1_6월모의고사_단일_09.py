from sympy import symbols, solve, Eq

x, y = symbols('x y', real=True)
eq1 = Eq(x - y, 3)
eq2 = Eq(2*x**2 + y**2, 6)

solutions = solve([eq1, eq2], [x, y])
alpha = solutions[0][0]
beta = solutions[0][1]

sum_val = alpha + beta
if sum_val == -1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')