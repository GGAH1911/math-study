import sympy as sp
from sympy import symbols, integrate, diff, sqrt, simplify

x = symbols('x', real=True)
a = sp.Rational(4, 7)

# Define f(x)
f = a/4 * x**4 - a/2 * x**2 + x + a/4 + 1

# Check condition (나): f(-1) = 0
f_at_minus1 = f.subs(x, -1)
if f_at_minus1 == 0:
    print('Condition (나) check: f(-1) =', f_at_minus1, '✓')
else:
    print('VERIFY_FAIL')
    exit()

# Check condition (다): f(x) >= k*x with k = f'(√2)
f_prime = diff(f, x)
k = f_prime.subs(x, sqrt(2))
k_simplified = simplify(k)

# Verify f(√2) = k√2
f_at_sqrt2 = f.subs(x, sqrt(2))
k_sqrt2 = k_simplified * sqrt(2)
if simplify(f_at_sqrt2 - k_sqrt2) == 0:
    print('f(√2) = k√2: ✓')
else:
    print('VERIFY_FAIL')
    exit()

# Verify f(x) - k*x ≥ 0
ineq_expr = f - k_simplified * x
ineq_simplified = simplify(ineq_expr)
print('f(x) - kx at x=√2:', simplify(ineq_simplified.subs(x, sqrt(2))))

# Calculate f(6)
f_at_6 = f.subs(x, 6)
result = int(f_at_6)
if result == 182:
    print('f(6) =', result)
    print('VERIFY_PASS')
else:
    print('f(6) =', result)
    print('VERIFY_FAIL')