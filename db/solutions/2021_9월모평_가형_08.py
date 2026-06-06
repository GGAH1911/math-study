import sympy as sp
n_var = sp.Symbol('n', integer=True, positive=True)
a1, r = sp.Rational(1, 2), 3
a_n = a1 * r**(n_var - 1)
limit_expr = 3**n_var / (a_n + 2**n_var)
lim_result = sp.limit(limit_expr, n_var, sp.oo)
if lim_result == 6:
    sum_result = 2 * sp.Rational(1, 1 - sp.Rational(1, 3))
    if sum_result == 3:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')