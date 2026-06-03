import sympy as sp
from sympy import sqrt, symbols, expand, simplify

alpha = 2 + sqrt(3)
beta = 2 * alpha

b = 1 - 6 * alpha
c = 4 * alpha**2
d = 2 * alpha + 1
e = -alpha**2

f = lambda x: 2*x**2 + b*x + c
g = lambda x: -x**2 + d*x + e

x = symbols('x')

# f(x) = x at alpha
f_val_alpha = f(alpha)
assert simplify(f_val_alpha - alpha) == 0, 'f(alpha) != alpha'

# f(x) = x at beta
f_val_beta = f(beta)
assert simplify(f_val_beta - beta) == 0, 'f(beta) != beta'

# g(x) = x at alpha (should be double root)
g_val_alpha = g(alpha)
assert simplify(g_val_alpha - alpha) == 0, 'g(alpha) != alpha'

# OP = PQ check
OP_sq = alpha**2 + alpha**2
PQ_sq = (beta - alpha)**2 + (beta - alpha)**2
assert simplify(OP_sq - PQ_sq) == 0, 'OP != PQ'

# f(x) + g(x) >= 0 for all x
h = 2*x**2 + (1-6*alpha)*x + 4*alpha**2 - x**2 + (2*alpha+1)*x - alpha**2
h = expand(h)
discriminant = simplify((2-4*alpha)**2 - 4*3*alpha**2)
assert simplify(discriminant) <= 0, 'f(x)+g(x) not non-negative'

print('VERIFY_PASS')