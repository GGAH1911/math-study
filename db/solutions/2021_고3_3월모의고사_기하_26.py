from sympy import symbols, solve, sqrt, simplify

x, y = symbols('x y', real=True)

eq1 = (x - 5)**2 + y**2 - 16
eq2 = (x + 5)**2 + y**2 - 100

solutions = solve([eq1, eq2], [x, y])

for sol in solutions:
    x_val, y_val = sol
    if x_val > 0 and y_val > 0:
        hyp_check = simplify(x_val**2 / 9 - y_val**2 / 16 - 1)
        dist_af = simplify(sqrt((x_val - 5)**2 + y_val**2))
        dist_af_prime = simplify(sqrt((x_val + 5)**2 + y_val**2))
        area = simplify(5 * y_val)
        
        if hyp_check == 0 and dist_af == 4 and dist_af_prime == 10:
            if simplify(area - 8*sqrt(6)) == 0:
                print('VERIFY_PASS')
            else:
                print('VERIFY_FAIL')