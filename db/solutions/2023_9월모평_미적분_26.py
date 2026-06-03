import sympy as sp
x, k = sp.symbols('x k', positive=True)
y = sp.sqrt(k*x/(2*x**2+1))
area = y**2
V = sp.integrate(area, (x, 1, 2))
k_val = sp.solve(sp.Eq(V, 2*sp.ln(3)), k)[0]
print('VERIFY_PASS' if sp.simplify(k_val - 8) == 0 else 'VERIFY_FAIL')
