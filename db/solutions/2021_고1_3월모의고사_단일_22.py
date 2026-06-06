from sympy import symbols, Eq, solve
x = symbols('x')
eq = Eq((5 - x) / 2, x - 8)
solution = solve(eq, x)
print('VERIFY_PASS' if solution == [7] else 'VERIFY_FAIL')