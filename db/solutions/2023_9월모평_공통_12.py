import sympy as sp
t, x = sp.symbols('t x', real=True)
# Original equations from the problem
roots = sp.solve(x**2 - (x + t), x)
# A has positive x-coordinate
a_expr = sp.Piecewise((roots[0], roots[0] > 0), (roots[1], True))
# Pick the larger root explicitly: (1+sqrt(1+4t))/2
a = (1 + sp.sqrt(1 + 4*t)) / 2
b = (1 - sp.sqrt(1 + 4*t)) / 2
# Verify these satisfy original equation y = x^2 = x + t
assert sp.simplify(a**2 - (a + t)) == 0
assert sp.simplify(b**2 - (b + t)) == 0
# A=(a,a^2), B=(b,b^2). C is on y=x^2 with y=a^2, x!=a => C=(-a, a^2)
C = (-a, a**2)
assert sp.simplify(C[1] - C[0]**2) == 0
# H = foot of perpendicular from B=(b,b^2) to horizontal line y=a^2
H = (b, a**2)
# Distances AH and CH
A_pt = (a, a**2)
B_pt = (b, b**2)
AH = sp.sqrt((A_pt[0]-H[0])**2 + (A_pt[1]-H[1])**2)
CH = sp.sqrt((C[0]-H[0])**2 + (C[1]-H[1])**2)
expr = (AH - CH) / t
L = sp.limit(expr, t, 0, '+')
print('limit =', L)
if sp.simplify(L - 2) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
