import sympy as sp
x = sp.Symbol('x')
eq = sp.Eq(4**x, (sp.Rational(1,2))**(x-9))
sol = sp.solve(eq, x)
if 3 in sol:
    lhs = 4**3
    rhs = (0.5)**(3-9)
    if abs(lhs - rhs) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')