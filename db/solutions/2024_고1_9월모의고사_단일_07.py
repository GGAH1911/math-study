import sympy as sp
k = -3
x = sp.Symbol('x')
eq = x**2 - x + k
roots = sp.solve(eq, x)
alpha, beta = roots[0], roots[1]
result = alpha**3 + beta**3
if abs(result - 10) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')