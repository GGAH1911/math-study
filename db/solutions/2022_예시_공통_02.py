import sympy as sp
x, a = sp.symbols('x a')
f = x**3 + a
integral_result = sp.integrate(f, (x, -1, 1))
eq = sp.Eq(integral_result, 4)
a_solution = sp.solve(eq, a)[0]
print('VERIFY_PASS' if a_solution == 2 else 'VERIFY_FAIL')