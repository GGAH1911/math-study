import sympy as sp
from sympy import symbols, solve, I

x = symbols('x')
eq = x**2 + 2*x + 3
roots = solve(eq, x)
alpha, beta = roots[0], roots[1]

result = (alpha**2 + 3*alpha + 3)/(alpha + 1) + (beta**2 + 3*beta + 3)/(beta + 1)
result_simplified = sp.simplify(result)

if result_simplified == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')