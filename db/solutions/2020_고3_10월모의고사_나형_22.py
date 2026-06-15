import sympy as sp
# ∫₀³ x² dx ?
CANDIDATE = 9
x = sp.symbols('x')
print('VERIFY_PASS' if sp.integrate(x**2, (x, 0, 3)) == CANDIDATE else 'VERIFY_FAIL')
