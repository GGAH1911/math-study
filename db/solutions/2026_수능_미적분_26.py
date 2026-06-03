import sympy as sp
x = sp.symbols('x', positive=True)
side = sp.sqrt(x + x*sp.ln(x))
A = sp.sqrt(3)/4 * side**2
V = sp.integrate(A, (x, 1, 2))
V = sp.simplify(V)
candidate = sp.sqrt(3)*(3 + 8*sp.ln(2))/16
if sp.simplify(V - candidate) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', V, candidate)
