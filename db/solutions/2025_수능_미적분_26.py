import sympy as sp
x = sp.symbols('x', positive=True)
integrand = (x + 1) / (x * (x + sp.ln(x)))
V = sp.integrate(integrand, (x, 1, sp.E))
expected = sp.ln(sp.E + 1)
if sp.simplify(V - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
