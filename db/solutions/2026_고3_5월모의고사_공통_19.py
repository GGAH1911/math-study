import sympy as sp
x = sp.Symbol('x')
a_val = 10
f = x**3 - 3*a_val*x**2 + 40*a_val**2
roots = sp.solve(f, x)
positive_roots = [r for r in roots if r.is_real and r > 0]
distinct_count = len(set(positive_roots))
if distinct_count == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')