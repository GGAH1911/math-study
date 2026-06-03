import sympy as sp

x = sp.Symbol('x', real=True)
t = sp.Symbol('t', real=True)

# f(x) = (x-2)^2
f_expr = (x - 2)**2

# g for x >= 0: integral_0^x t*(t-2)^2 dt
g_pos = sp.integrate(t * (t - 2)**2, (t, 0, x))
g_pos = sp.expand(g_pos)  # x^4/4 - 4x^3/3 + 2x^2

# Verify g(2) = 4/3
g_at_2 = g_pos.subs(x, 2)
assert g_at_2 == sp.Rational(4, 3), f'g(2)={g_at_2}'

# g'(x) for x >= 0
g_prime_pos = sp.diff(g_pos, x)  # x(x-2)^2

# g'(2) must be 0
g_prime_at_2 = g_prime_pos.subs(x, 2)
assert g_prime_at_2 == 0, f"g'(2)={g_prime_at_2}"

# a values
a1 = -2 * sp.sqrt(3) / 3
a2 = sp.Integer(2)

# g(a1) = a1^2 (since a1 < 0)
g_a1 = a1**2
assert sp.simplify(g_a1 - sp.Rational(4, 3)) == 0, f'g(a1)={sp.simplify(g_a1)}'

# g(a2) = 4/3
g_a2 = g_pos.subs(x, a2)
assert g_a2 == sp.Rational(4, 3), f'g(a2)={g_a2}'

# g'(a1) != 0 (so h not differentiable at x1 = a1)
g_prime_a1 = (2 * a1)  # g'(x)=2x for x<0
assert sp.simplify(g_prime_a1) != 0

# Product of all a values
product = sp.simplify(a1 * a2)
expected = -4 * sp.sqrt(3) / 3
assert sp.simplify(product - expected) == 0, f'product={product}'

print('VERIFY_PASS')
