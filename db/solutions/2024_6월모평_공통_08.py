from sympy import symbols, solve, expand
x = symbols('x')
k = 3
eq = x**3 - 3*x**2 + k + 1
roots = solve(eq, x)
valid_roots = [r for r in roots if r.is_real]
if len(valid_roots) == 2:
    x_vals = sorted([float(r) for r in valid_roots])
    for x_val in x_vals:
        y1 = 2*x_val**2 - 1
        y2 = x_val**3 - x_val**2 + k
        if abs(y1 - y2) > 1e-9:
            print('VERIFY_FAIL')
            exit()
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')