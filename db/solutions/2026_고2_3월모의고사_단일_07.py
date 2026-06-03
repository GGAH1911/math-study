import sympy as sp
x = sp.Symbol('x')
eq = x**3 - 7*x + 6
roots = sp.solve(eq, x)
positive_roots = [r for r in roots if r.is_real and r > 0]
sum_positive = sum(positive_roots)
if sum_positive == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')