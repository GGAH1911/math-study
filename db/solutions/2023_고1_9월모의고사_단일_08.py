from sympy import symbols, expand, solve, I, sqrt
x = symbols('x')
eq = x**2 + 2*x + 7
roots = solve(eq, x)
alpha, beta = roots[0], roots[1]
result = alpha**2 + alpha*beta + beta**2
result_simplified = expand(result)
print('VERIFY_PASS' if result_simplified == -3 else 'VERIFY_FAIL')