from sympy import *
k = -2
x = symbols('x')
eq = x**2 + k*x - Rational(1,2)*k**2 + 3*k
roots = solve(eq, x)
alpha, beta = roots[0], roots[1]
result = (alpha**2 - k*beta - 12)
print('VERIFY_PASS' if simplify(result) == 0 else 'VERIFY_FAIL')