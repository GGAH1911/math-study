import sympy as sp
x = sp.symbols('x', positive=True)
side = sp.sqrt((5-x)*sp.ln(x))
area = side**2
V = sp.integrate(area, (x, 2, 4))
V_simplified = sp.simplify(V)
candidate = 16*sp.ln(2) - 7
print('VERIFY_PASS' if sp.simplify(V_simplified - candidate) == 0 else 'VERIFY_FAIL')