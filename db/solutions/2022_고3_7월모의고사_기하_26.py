import sympy as sp
x, y = sp.symbols('x y', real=True)
k_val = 12
c_val = sp.sqrt(4 + k_val)  # c^2 = a^2 + b^2 for hyperbola
# Hyperbola: x^2/4 - y^2/k = 1
hyperbola = x**2/4 - y**2/k_val - 1
# Point P in first quadrant on hyperbola with tangent x-intercept = 4/3
# Tangent at (x1,y1): x*x1/4 - y*y1/k = 1; y=0 -> x = 4/x1 = 4/3 -> x1 = 3
x1 = sp.Rational(3)
y1_sq = sp.solve(hyperbola.subs(x, x1), y**2)[0]
y1 = sp.sqrt(y1_sq)  # first quadrant: positive
# Check P on hyperbola
assert sp.simplify(hyperbola.subs([(x, x1), (y, y1)])) == 0
# Tangent line x-intercept
tangent_xint = sp.Rational(4) / x1
assert tangent_xint == sp.Rational(4, 3)
# |PF'| = |FF'|
F = sp.Matrix([c_val, 0])
Fp = sp.Matrix([-c_val, 0])
P = sp.Matrix([x1, y1])
PFp = sp.sqrt((P - Fp).dot(P - Fp))
FFp = sp.sqrt((F - Fp).dot(F - Fp))
if sp.simplify(PFp - FFp) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
