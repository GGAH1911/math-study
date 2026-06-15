import sympy as sp
from sympy import ln, exp, sqrt, symbols, diff, solve, simplify

x, t = symbols('x t', positive=True, real=True)

# Define f(x)
f = ln(x) / x
f_prime = diff(f, x)
f_double_prime = diff(f_prime, x)

# Find x0 where tangent from origin touches curve
# Condition: f(x0)/x0 = f'(x0)
eq = f.subs(x, x) / x - f_prime.subs(x, x)
x0_solutions = solve(ln(x) - (1 - ln(x)), x)
x0 = exp(sp.Rational(1, 2))

# Verify x0 = sqrt(e)
assert simplify(f.subs(x, x0) / x0 - f_prime.subs(x, x0)) == 0

# Calculate a = f'(sqrt(e))
a_val = f_prime.subs(x, x0)
a_val_simplified = simplify(a_val)

# At t=a, g(a) = sqrt(e)
# From f'(g(t)) = t, differentiating: f''(g(t)) * g'(t) = 1
# So g'(a) = 1/f''(sqrt(e))
f_double_prime_at_x0 = f_double_prime.subs(x, x0)
f_double_prime_simplified = simplify(f_double_prime_at_x0)

g_prime_a = 1 / f_double_prime_simplified
g_prime_a_simplified = simplify(g_prime_a)

# Calculate a * g'(a)
result = simplify(a_val_simplified * g_prime_a_simplified)

if simplify(result + sqrt(exp(1))/4) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Result: {result}')