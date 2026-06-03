import sympy as sp
x = sp.Symbol('x')
f = x**3 - 2*x**2 + 4*x
f_prime = sp.diff(f, x)
lhs = x*f_prime - 3*f
rhs = 2*x**2 - 8*x
equation_satisfied = sp.simplify(lhs - rhs) == 0
f_at_1 = f.subs(x, 1)
if equation_satisfied and f_at_1 == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')