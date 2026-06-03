import sympy as sp
x = sp.symbols('x')
val = sp.integrate((x+2)/(x+1), (x, 0, 10))
candidate = 10 + sp.ln(11)
print('VERIFY_PASS' if sp.simplify(val - candidate) == 0 else 'VERIFY_FAIL')
