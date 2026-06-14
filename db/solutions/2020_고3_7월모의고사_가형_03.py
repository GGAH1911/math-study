import sympy as sp
n = sp.Symbol('n', positive=True, integer=True)

left_expr = (3*n**2 - n) / (n**2 + 1)
right_expr = (3*n**2 + 2*n) / (n**2 + 1)

left_limit = sp.limit(left_expr, n, sp.oo)
right_limit = sp.limit(right_expr, n, sp.oo)

if left_limit == 3 and right_limit == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')