import sympy as sp

CANDIDATE = 24

x = sp.Symbol('x')

# g(x) = x^2 - 1
g = x**2 - 1

# Verify g(1) = 0
assert g.subs(x, 1) == 0, "g(1) must be 0"

# Verify g(-1) = 0  
assert g.subs(x, -1) == 0, "g(-1) must be 0"

# Verify leading coefficient is 1
assert sp.Poly(g, x).LC() == 1, "Leading coefficient must be 1"

# Calculate g(5)
g_5 = g.subs(x, 5)
assert g_5 == CANDIDATE, f"g(5) = {g_5} but CANDIDATE = {CANDIDATE}"

print('VERIFY_PASS')