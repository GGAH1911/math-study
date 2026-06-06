from sympy import symbols, log, sqrt, solve, simplify

x, y = symbols('x y', positive=True, real=True)
eq1 = log(x + 2*y, 2) - 3
eq2 = log(x, 2) + log(y, 2) - 1

sols = solve([eq1, eq2], [x, y])
result = sum(s[0]**2 + 4*s[1]**2 for s in sols)
result_simplified = simplify(result / len(sols))

for sol in sols:
    x_val, y_val = sol
    check1 = simplify(log(x_val + 2*y_val, 2)) == 3
    check2 = simplify(log(x_val, 2) + log(y_val, 2)) == 1
    value = simplify(x_val**2 + 4*y_val**2)
    if check1 and check2 and value == 56:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')