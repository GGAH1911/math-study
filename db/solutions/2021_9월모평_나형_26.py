from sympy import symbols, expand, roots
x = symbols('x')
k = 12
f = x**3 - x**2 - 8*x + k
roots_dict = roots(f, x)
distinct_roots = len([r for r in roots_dict.keys() if roots_dict[r] > 0])
if distinct_roots == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')