import sympy as sp
x, a = sp.symbols('x a')
eq = x**2 + 10*x + 25
roots = sp.solve(eq, x)
print('VERIFY_PASS' if len(roots) == 1 and roots[0] == -5 else 'VERIFY_FAIL')