import sympy as sp
x = sp.symbols('x', real=True)
a_val, b_val = 6, 3
expr = (2**(a_val*x + b_val) - 8) / (2**(b_val*x) - 1)
limit_val = sp.limit(expr, x, 0)
if sp.simplify(limit_val - 16) == 0 and (a_val + b_val) == 9 and a_val != 0 and b_val != 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
