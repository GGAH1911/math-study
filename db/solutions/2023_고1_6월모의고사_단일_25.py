import sympy as sp
x = sp.Symbol('x')
roots = sp.solve(x**2 - 6*x + 11, x)
alpha, beta = roots[0], roots[1]
result = 11 * (alpha/beta + beta/alpha)
result_simplified = sp.simplify(result)
print('VERIFY_PASS' if result_simplified == 14 else 'VERIFY_FAIL')