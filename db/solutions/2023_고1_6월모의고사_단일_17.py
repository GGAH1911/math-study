from sympy import symbols, solve, simplify

a = 2
alpha, beta = symbols('alpha beta', real=True)

eq1 = alpha + beta - 1/a
eq2 = alpha * beta + 6/a
eq3 = beta - alpha - 7/2

sols = solve([eq1, eq2, eq3], [alpha, beta])
print(f'Solutions: {sols}')

for sol in sols:
    if sol[1] > sol[0]:  # alpha < beta
        alpha_val, beta_val = sol
        result = simplify(alpha_val**2 + beta_val**2)
        print(f'alpha = {alpha_val}, beta = {beta_val}')
        print(f'alpha^2 + beta^2 = {result}')
        
        if result == 25/4:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')