import sympy as sp
from sympy import symbols, expand, solve, lambdify

x = symbols('x')
f = sp.Rational(1, 2) * (x - 1)**2 * (x - 4) + 1

# Check f(1) = f(4) = 1
f_1 = f.subs(x, 1)
f_4 = f.subs(x, 4)
f_0 = f.subs(x, 0)

# Check f'(x) roots
f_prime = sp.diff(f, x)
f_prime_roots = solve(f_prime, x)

# Verify conditions
assert f_1 == 1, f'f(1) = {f_1}, expected 1'
assert f_4 == 1, f'f(4) = {f_4}, expected 1'
assert f_0 == -1, f'f(0) = {f_0}, expected -1'
assert len(f_prime_roots) == 2, f'f\'(x) should have 2 roots'
assert abs(f_prime_roots[1] - f_prime_roots[0]) == 2, f'root difference should be 2'

# Calculate f(5)
f_5 = f.subs(x, 5)
print(f'VERIFY_PASS')