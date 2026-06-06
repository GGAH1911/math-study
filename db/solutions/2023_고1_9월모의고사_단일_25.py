import sympy as sp
p_val = 10
x = sp.Symbol('x')
eq = x**2 - p_val*x + (p_val + 19)
roots = sp.solve(eq, x)
for root in roots:
    if sp.im(root) == 2:
        print('VERIFY_PASS')
        break
else:
    print('VERIFY_FAIL')