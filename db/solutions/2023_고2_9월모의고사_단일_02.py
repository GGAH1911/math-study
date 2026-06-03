import sympy as sp
x = sp.Symbol('x')
expr = (x-2)*(x**3+1)/(x-2)
limit_val = sp.limit(expr, x, 2)
result = 'VERIFY_PASS' if limit_val == 9 else 'VERIFY_FAIL'
print(result)