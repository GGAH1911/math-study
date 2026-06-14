import sympy as sp
x = sp.Symbol('x')
a = -6
b = 4
g = 2*x**3 + a*x + b

# Check g(1) = 0
assert g.subs(x, 1) == 0, 'g(1) should be 0'

# Left limit: lim (x->1-) g(x)/(x-1)
h_left = g / (x - 1)
lim_left = sp.limit(h_left, x, 1, '-')

# Right limit: lim (x->1+) [1/(2x+1)] * g(x) = [1/3] * g(1)
lim_right = sp.Rational(1, 3) * g.subs(x, 1)

# Function value at x=1
h_at_1 = sp.Rational(1, 3) * 0

# Verify continuity
if lim_left == lim_right == h_at_1 == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')