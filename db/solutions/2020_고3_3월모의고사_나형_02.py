import sympy as sp
x = sp.Symbol('x', real=True)
equation = sp.Eq(4**x, 64)
solutions = sp.solve(equation, x)
if solutions:
    x_val = solutions[0]
    result = 4**x_val
    if sp.simplify(result - 64) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')