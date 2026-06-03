import sympy as sp
x, y = sp.symbols('x y', real=True)
eq1 = x + y + x*y - 8
eq2 = 2*x + 2*y - x*y - 4
sols = sp.solve([eq1, eq2], [x, y])
for sol in sols:
    alpha, beta = sol[0], sol[1]
    result = alpha**2 + beta**2
    if result == 8:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')