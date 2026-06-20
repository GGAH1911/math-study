import sympy as sp
from sympy import symbols, integrate, diff

CANDIDATE = 5

x, a, t = symbols('x a t', real=True)

# f(x) = -x^2 - 4x + a
f = -t**2 - 4*t + CANDIDATE

# g(x) = integral from 0 to x of f(t) dt
g = integrate(f, (t, 0, x))

# g'(x) should equal f(x)
g_prime = diff(g, x)
f_at_x = -x**2 - 4*x + CANDIDATE

# Verify g'(x) = f(x)
assert sp.simplify(g_prime - f_at_x) == 0, 'g_prime != f'

# Check that g'(x) >= 0 for all x in [0, 1]
# g'(x) = -x^2 - 4x + 5 = -(x^2 + 4x - 5) = -(x+5)(x-1)
quadratic = -x**2 - 4*x + CANDIDATE
roots = sp.solve(quadratic, x)
# roots should be -5 and 1
assert sorted([float(r) for r in roots]) == [-5.0, 1.0]

# For x in [0, 1], evaluate at critical points
for test_x in [0, 0.5, 1]:
    val = float(quadratic.subs(x, test_x))
    assert val >= -1e-10, f'g\'({test_x}) = {val} < 0'

# g'(1) should equal 0 (boundary)
assert float(quadratic.subs(x, 1)) == 0

print('VERIFY_PASS')