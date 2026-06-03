import sympy as sp
x = sp.Symbol('x')
f = x + sp.ln(x)
integrand = (1 + 1/x) * f
result = sp.integrate(integrand, (x, 1, sp.E))
option2 = sp.E**2/2 + sp.E
if sp.simplify(result - option2) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')