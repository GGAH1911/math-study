import sympy as sp
from sympy import symbols, solve, simplify

k = sp.Rational(3, 2)
x = symbols('x', real=True)

# Define f(x) and g(x)
f = x**2 + 2*x + k
g_expr = 2*x**3 - 9*x**2 + 12*x - 2

# Compute (g ∘ f)(x)
g_of_f = g_expr.subs(x, f)
g_of_f_simplified = simplify(g_of_f)

# Find the minimum by taking derivative
derivative = sp.diff(g_of_f_simplified, x)
critical_points = solve(derivative, x)

# Evaluate g(f(x)) at critical points and endpoints
values = []
for cp in critical_points:
    values.append((cp, g_of_f_simplified.subs(x, cp)))

min_value = min([simplify(v[1]) for v in values])

if min_value == 2:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: minimum is {min_value}, expected 2')