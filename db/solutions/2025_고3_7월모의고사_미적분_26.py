import sympy as sp
t = sp.Symbol('t', positive=True)
f = (sp.ln(t) - t) / t**2
result = sp.integrate(f, (t, 1, sp.E))
expected = -2 / sp.E
if sp.simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')