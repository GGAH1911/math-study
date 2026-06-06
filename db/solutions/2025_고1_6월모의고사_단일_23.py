from sympy import symbols, solve, simplify
x = symbols('x')
eq = x**4 - 2*x**3 - x**2 + 2*x
roots = solve(eq, x)
positive_roots = [r for r in roots if r.is_real and r > 0]
sum_positive = sum(positive_roots)
print('VERIFY_PASS' if sum_positive == 3 else 'VERIFY_FAIL')