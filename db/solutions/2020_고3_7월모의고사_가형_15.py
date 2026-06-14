from sympy import symbols, diff, simplify

x = symbols('x')

# Define g(x) satisfying: g(2)=2, g'(2)=2, g''(2)=0, g is increasing
g = 2 + 2*(x-2) + (x-2)**3
g_prime = diff(g, x)
g_double_prime = diff(g_prime, x)

# Verify g conditions
assert g.subs(x, 2) == 2, "g(2) must be 2"
assert g_prime.subs(x, 2) == 2, "g'(2) must be 2"
assert g_double_prime.subs(x, 2) == 0, "g''(2) must be 0"
assert all(g_prime.subs(x, val) > 0 for val in [-10, -5, 0, 5, 10]), "g must be increasing"

# Define f(x) such that f'(2)=4; use f(x)=x^2
f = lambda u: u**2
f_prime = lambda u: 2*u
f_double_prime_val = 2

assert f_prime(2) == 4, "f'(2) must be 4"

# Compute h(x) = f(g(x))
h = f(g)
h_prime = diff(h, x)
h_double_prime = diff(h_prime, x)

# Evaluate at x=2
h_prime_at_2 = h_prime.subs(x, 2)
h_double_prime_at_2 = h_double_prime.subs(x, 2)

# Verify the condition h''(2)/f''(2) = 4
ratio = simplify(h_double_prime_at_2 / f_double_prime_val)
assert ratio == 4, f"h''(2)/f''(2) must be 4, got {ratio}"

# Check answer
CANDIDATE = 8
if h_prime_at_2 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')