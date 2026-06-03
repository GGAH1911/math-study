import sympy as sp
x = sp.Symbol('x')
f = 12 / (x - 1)
cond = sp.limit((x - 1) * f, x, sp.oo)
if cond == 12:
    expr = ((x**2 - 1) * f) / (3*x + 1)
    result = sp.limit(expr, x, sp.oo)
    if result == 4:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')