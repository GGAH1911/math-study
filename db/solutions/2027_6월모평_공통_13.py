from sympy import symbols, integrate, diff
import sympy as sp

t = symbols('t', real=True, positive=True)
a = 2

# S(t) = t^3/3 - t^2 + 2t
S = t**3/3 - t**2 + 2*t

# Verify S'(t) = t^2 - 2t + a
S_prime = diff(S, t)
expected_S_prime = t**2 - 2*t + a

assert S_prime == expected_S_prime, f'S\'(t) mismatch: {S_prime} vs {expected_S_prime}'

# Verify S(3) = 6
S_3 = S.subs(t, 3)
assert S_3 == 6, f'S(3) = {S_3}, expected 6'

# Verify S(4)
S_4 = S.subs(t, 4)
expected_S_4 = sp.Rational(40, 3)
assert S_4 == expected_S_4, f'S(4) = {S_4}, expected {expected_S_4}'

# Verify integral from -2 to 2 equals S(4)
x = symbols('x', real=True)
integral_result = integrate(x**2 - 2*x + 2, (x, -2, 2))
assert integral_result == expected_S_4, f'Integral = {integral_result}, expected {expected_S_4}'

print('VERIFY_PASS')