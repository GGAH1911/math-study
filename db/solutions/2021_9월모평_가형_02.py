import sympy as sp
n = sp.Symbol('n', positive=True, integer=True)
numerator = (2*n + 1)**2 - (2*n - 1)**2
denominator = 2*n + 5
expression = numerator / denominator
limit_value = sp.limit(expression, n, sp.oo)
if limit_value == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')