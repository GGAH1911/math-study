import sympy as sp
x = sp.symbols('x')
expr = (sp.exp(7*x) - 1)/x
val = sp.limit(expr, x, 0)
ans = 7
print('VERIFY_PASS' if sp.simplify(val - ans) == 0 else 'VERIFY_FAIL')