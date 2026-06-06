from sympy import symbols, solve, simplify

x, y = symbols('x y')
eq1 = 3*x - 2*y - 7
eq2 = 6*x**2 - x*y - 2*y**2

sols = solve([eq1, eq2], [x, y])

for sol in sols:
    alpha, beta = sol[0], sol[1]
    check1 = 3*alpha - 2*beta - 7
    check2 = 6*alpha**2 - alpha*beta - 2*beta**2
    if simplify(check1) == 0 and simplify(check2) == 0:
        result = alpha - beta
        if simplify(result) == 3:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')