import sympy as sp
k = sp.Symbol('k', real=True, positive=True)
v = lambda t: 2*t - 6
distance = sp.integrate(v(sp.Symbol('t')), (sp.Symbol('t'), 3, k))
eq = sp.Eq(distance, 25)
sol = sp.solve(eq, k)
print('Solutions:', sol)
k_val = 8
result = sp.integrate(2*sp.Symbol('t') - 6, (sp.Symbol('t'), 3, k_val))
if result == 25:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')