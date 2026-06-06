import sympy as sp
u = sp.Symbol('u')
f = (u - 1) * (u - 1/sp.sqrt(2))**2 + sp.Rational(1, 2)
result = f.subs(u, 2)
result_simplified = sp.simplify(result)
expected_form = 5 - 2*sp.sqrt(2)
if sp.simplify(result_simplified - expected_form) == 0:
    a, b = 5, -2
    answer = a**2 + b**2
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')