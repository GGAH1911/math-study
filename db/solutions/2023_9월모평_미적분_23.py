import sympy as sp
x = sp.Symbol('x')
expr = (4**x - 2**x) / x
limit_val = sp.limit(expr, x, 0)
expected = sp.log(2)
if sp.simplify(limit_val - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')