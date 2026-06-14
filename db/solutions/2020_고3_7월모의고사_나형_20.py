from sympy import *
x = symbols('x')

# h(x) = x³/3 - x² + 4/3
h = x**3/3 - x**2 + Rational(4,3)

# 검증 1: h(-1) = 0
assert h.subs(x, -1) == 0, f"h(-1) = {h.subs(x, -1)}"

# 검증 2: h(2) = 0
assert h.subs(x, 2) == 0, f"h(2) = {h.subs(x, 2)}"

# 검증 3: h(0) > 0
assert h.subs(x, 0) > 0, f"h(0) = {h.subs(x, 0)}"

# 검증 4: h'(x) = x(x-2)
h_prime = diff(h, x)
expected_h_prime = x*(x - 2)
assert expand(h_prime - expected_h_prime) == 0

# 검증 5: ∫_{-1}^{1} h(x)dx = 2
integral_result = integrate(h, (x, -1, 1))
assert integral_result == 2, f"Integral = {integral_result}"

print('VERIFY_PASS')