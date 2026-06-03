import sympy as sp
x, y = sp.symbols('x y')
eq1 = x - y + 3
eq2 = x**2 - 6*x + 4*y - 11
sols = sp.solve([eq1, eq2], [x, y])
print('Solutions:', sols)
for sol in sols:
    alpha, beta = sol
    result = alpha + beta
    check1 = alpha - beta + 3
    check2 = alpha**2 - 6*alpha + 4*beta - 11
    if check1 == 0 and check2 == 0 and result == 5:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')