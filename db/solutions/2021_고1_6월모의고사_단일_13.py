from sympy import symbols, solve, Eq
x, y = symbols('x y', real=True)
eq1 = Eq(2*x - 3*y, -1)
eq2 = Eq(x**2 - 2*y**2, -1)
solutions = solve([eq1, eq2], [x, y])
for sol in solutions:
    if sol[0] != sol[1]:
        alpha, beta = sol[0], sol[1]
        check1 = 2*alpha - 3*beta + 1
        check2 = alpha**2 - 2*beta**2 + 1
        if check1 == 0 and check2 == 0 and alpha + beta == 12:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')