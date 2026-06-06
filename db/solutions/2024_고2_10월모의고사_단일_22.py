import sympy as sp
x = sp.Symbol('x')
eq = (3**(sp.Rational(1,2)))**(x-2) - 27
result = sp.solve(eq, x)
if result:
    ans = result[0]
    check = (3**(sp.Rational(1,2)))**(ans-2) - 27
    if sp.simplify(check) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')