import sympy as sp
x, y = sp.symbols('x y')
eq1 = 4*x**2 - y**2 - 27
eq2 = 2*x + y - 3
sols = sp.solve([eq1, eq2], [x, y])
for sol in sols:
    x_val, y_val = sol
    check1 = 4*x_val**2 - y_val**2
    check2 = 2*x_val + y_val
    if check1 == 27 and check2 == 3:
        if x_val - y_val == 6:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')