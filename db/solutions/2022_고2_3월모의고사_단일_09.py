import sympy as sp
x, y = sp.symbols('x y')
eq1 = sp.Eq(x + y, sp.sqrt(2))
eq2 = sp.Eq(x * y, -2)
sols = sp.solve([eq1, eq2], [x, y])
result = -4*sp.sqrt(2)
for sol in sols:
    x_val, y_val = sol
    calc = x_val**2 / y_val + y_val**2 / x_val
    calc_simplified = sp.simplify(calc)
    if sp.simplify(calc_simplified - result) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')