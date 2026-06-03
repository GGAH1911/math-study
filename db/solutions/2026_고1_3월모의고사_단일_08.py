import sympy as sp
x = sp.Symbol('x')
eq = 3*x**2 - 3*x - 1
ans = (3 + sp.sqrt(21))/6
result = eq.subs(x, ans)
result_simplified = sp.simplify(result)
if result_simplified == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')