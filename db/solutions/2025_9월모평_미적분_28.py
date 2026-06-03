import sympy as sp

x, t = sp.symbols('x t', real=True)
# Concrete f satisfying all hypotheses: f(x)=c*x with c chosen so that
# int_0^1 f'(2x) sin(pi x) dx = 1/12.
c = sp.pi / sp.Integer(24)
f = c * t
fp = sp.diff(f, t)  # constant c, continuous derivatives of all orders

# g(x) = f'(2x) sin(pi x) + x with this c
gx = fp.subs(t, 2*x) * sp.sin(sp.pi * x) + x
# Strictly increasing? g'(x) = c*pi*cos(pi x) + 1, min = 1 - c*pi = 1 - pi^2/24 > 0
min_gprime = 1 - sp.pi * c
assert sp.simplify(min_gprime) > 0

# Endpoints
assert sp.simplify(gx.subs(x, 0)) == 0
assert sp.simplify(gx.subs(x, 1)) == 1

# Use area identity for inverse: int_0^1 g + int_0^1 g^{-1} = 1
int_g = sp.integrate(gx, (x, 0, 1))
int_ginv = 1 - int_g

# Verify the given integral condition with the ORIGINAL expressions
int_fp_sin = sp.integrate(fp.subs(t, 2*x) * sp.sin(sp.pi * x), (x, 0, 1))
LHS = sp.simplify(int_ginv)
RHS = sp.simplify(2 * int_fp_sin + sp.Rational(1, 4))
cond_ok = sp.simplify(LHS - RHS) == 0

# Compute target integral from ORIGINAL problem
target = sp.integrate(f * sp.cos(sp.pi/2 * t), (t, 0, 2))
expected = -sp.Rational(1, 3) / sp.pi
ans_ok = sp.simplify(target - expected) == 0

print('VERIFY_PASS' if cond_ok and ans_ok else 'VERIFY_FAIL')