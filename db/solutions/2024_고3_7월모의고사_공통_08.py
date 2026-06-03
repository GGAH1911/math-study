import sympy as sp
x = sp.Symbol('x')
f = 2*x**3 - x - 1
f_prime = sp.diff(f, x)
f_0 = f.subs(x, 0)
lhs = x*f_prime
rhs = 6*x**3 - x + f_0 + 1
verify_eq = sp.expand(lhs - rhs)
if verify_eq == 0:
    result = f.subs(x, -1)
    if result == -2:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')