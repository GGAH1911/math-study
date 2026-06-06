import sympy as sp
x = sp.Symbol('x')
equation = 9**x - 10 * 3**(x+1) + 81
alpha, beta = 3, 1
result_alpha = equation.subs(x, alpha)
result_beta = equation.subs(x, beta)
if abs(result_alpha) < 1e-9 and abs(result_beta) < 1e-9:
    answer = alpha**2 + beta**2
    if answer == 10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')