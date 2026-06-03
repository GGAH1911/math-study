import sympy as sp
n = sp.Symbol('n', positive=True, integer=True)
a_n = 6 / (3*n + 2)
b_n = 2*n
product = a_n * b_n
limit_value = sp.limit(product, n, sp.oo)
cond1 = sp.limit((3*n + 2) * a_n, n, sp.oo)
cond2 = sp.limit(b_n / n, n, sp.oo)
if cond1 == 6 and cond2 == 2 and limit_value == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')