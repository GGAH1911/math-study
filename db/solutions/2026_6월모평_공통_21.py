CANDIDATE = '42'

from sympy import symbols, expand, Poly

x = symbols('x', real=True)

# From verified solution:
# f(x) = (x-1)(x-2)
# g(x) = (x-1)(x-2)h(x) where h(x) = x^2 - 3x + 3

f = (x - 1) * (x - 2)
h = x**2 - 3*x + 3
g = (x - 1) * (x - 2) * h

# Verify g is a quartic with leading coefficient 1
g_expanded = expand(g)
poly_g = Poly(g_expanded, x)
assert poly_g.LC() == 1, "g must have leading coefficient 1"
assert poly_g.degree() == 4, "g must be degree 4"

# Verify roots of g at x=1, x=2
assert g.subs(x, 1) == 0, "g(1) must equal 0"
assert g.subs(x, 2) == 0, "g(2) must equal 0"

# Verify h(1)=1, h(2)=1
assert h.subs(x, 1) == 1, "h(1) must equal 1"
assert h.subs(x, 2) == 1, "h(2) must equal 1"

# Verify h has no real roots (discriminant < 0)
discriminant = (-3)**2 - 4*1*3  # discriminant = -3
assert discriminant < 0, "h must have no real roots"

# Verify critical identity: g(x) - f(x) = (x-1)^2(x-2)^2
difference = expand(g - f)
expected_diff = expand((x - 1)**2 * (x - 2)**2)
assert difference == expected_diff, f"g-f must equal (x-1)^2(x-2)^2"

# Calculate the answer: g(-1)
answer = g.subs(x, -1)
# g(-1) = (-1-1)(-1-2)(1+3+3) = (-2)(-3)(7) = 42

# Verify against CANDIDATE
target_value = int(CANDIDATE)
if answer == target_value:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")